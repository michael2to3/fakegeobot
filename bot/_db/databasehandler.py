import logging
from typing import Iterable, Optional, cast, Generator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from contextlib import contextmanager
from model import User, Geolocation, Session as UserSession, ApiApp
from _cron import Cron
from _action import Fakelocation

Base = declarative_base()


class UserRecord(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    cron_expression = Column(String, nullable=True)
    cron_timeout = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    session_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)
    phone = Column(String)
    auth_code = Column(Integer)
    recipient = Column(String, nullable=True)
    phone_code_hash = Column(String)


class DatabaseHandler:
    logger: logging.Logger
    _name_db: str
    _path_db: str
    engine = None
    SessionLocal = None
    _instance = None
    _api: ApiApp

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, path_db: str, name_db: str, api: ApiApp):
        if not self.engine:
            self.logger = logging.getLogger(__name__)
            self._name_db = name_db
            self._path_db = path_db + "/" + self._name_db
            self.engine = create_engine(
                f"sqlite:///{self._path_db}", connect_args={"timeout": 30}
            )
            Base.metadata.create_all(bind=self.engine)
            self.SessionLocal = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            )
            self._api = api
        else:
            self.logger.warning("Trying to initialize DatabaseHandler again.")

    def save_user(self, user: User):
        user_record = UserRecord(
            cron_expression=(user.cron.expression if user.cron is not None else None),
            cron_timeout=user.cron.timeout if user.cron is not None else None,
            location=(user.location.to_json() if user.location is not None else None),
            session_name=user.session.session_name,
            username=user.session.username,
            chat_id=user.session.chat_id,
            phone=user.session.phone,
            auth_code=user.session.auth_code,
            recipient=user.recipient,
            phone_code_hash=user.session.phone_code_hash,
        )

        with self._get_session() as db_session:
            db_session.add(user_record)
            db_session.commit()

    def delete_user(self, chat_id: int):
        with self._get_session() as db_session:
            user_record = (
                db_session.query(UserRecord)
                .filter(UserRecord.chat_id == chat_id)
                .first()
            )
            if user_record:
                db_session.delete(user_record)
                db_session.commit()

    def load_all_users(self) -> Iterable[User]:
        with self._get_session() as db_session:
            users = db_session.query(UserRecord).all()
            for user_record in users:
                user = self._user_from_record(user_record)
                if user:
                    yield user

    def load_user(self, chat_id: int) -> Optional[User]:
        with self._get_session() as db_session:
            user_record = (
                db_session.query(UserRecord)
                .filter(UserRecord.chat_id == chat_id)
                .first()
            )
            if user_record:
                return self._user_from_record(user_record)
            else:
                raise ValueError("User not found")

    def user_exists(self, chat_id: int) -> bool:
        with self._get_session() as db_session:
            user_record = (
                db_session.query(UserRecord)
                .filter(UserRecord.chat_id == chat_id)
                .first()
            )
            return user_record is not None

    def _user_from_record(self, user_record: UserRecord) -> User:
        chat_id = cast(Optional[int], user_record.chat_id)
        auth_code = cast(Optional[int], user_record.auth_code)

        if chat_id is None:
            raise ValueError("User not found")

        session = UserSession(
            str(user_record.session_name),
            str(user_record.username),
            chat_id,
            str(user_record.phone),
            auth_code,
            str(user_record.phone_code_hash),
        )

        location = None
        if user_record.location is not None:
            location_str = str(user_record.location)
            location = Geolocation.from_json(location_str)

        recipient = cast(Optional[str], user_record.recipient)

        cron_expression = user_record.cron_expression
        cron_timeout = cast(Optional[int], user_record.cron_timeout)
        if (
            cron_expression is not None
            and recipient is not None
            and location is not None
            and cron_timeout is not None
        ):
            cron = Cron(
                expression=str(cron_expression),
                callback=Fakelocation(self._api, session, location, recipient).execute,
                timeout=cron_timeout,
            )
        else:
            cron = None

        user = User(cron, location, session, recipient)
        return user

    @contextmanager
    def _get_session(self) -> Generator[Session, None, None]:
        if self.SessionLocal is None:
            logging.getLogger(__name__).error("DatabaseHandler is not initialized")
            raise ValueError("DatabaseHandler is not initialized")
        session = self.SessionLocal()
        try:
            yield session
        finally:
            self.SessionLocal.remove()
