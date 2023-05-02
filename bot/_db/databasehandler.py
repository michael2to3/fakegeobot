import logging
from contextlib import contextmanager
from typing import Generator, Iterable, Optional, cast

from .._action import Fakelocation
from .._cron import Cron
from ..model import ApiApp, Geolocation, Session as UserSession, User
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

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
    language = Column(String)


class DatabaseHandler:
    logger: logging.Logger
    engine = None
    SessionLocal = None
    _instance = None
    _api: ApiApp
    _url: str

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api: ApiApp, uri: str):
        if not self.engine:
            self.logger = logging.getLogger(__name__)
            self.engine = create_engine(
                uri,
                connect_args={"timeout": 30},
                poolclass=NullPool,
            )
            self.SessionLocal = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            )
            self._api = api
            Base.metadata.create_all(bind=self.engine)
        else:
            self.logger.warning("Database already initialized")

    def close(self):
        if self.engine:
            self.engine.dispose()

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
            language=user.language,
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
        language = cast(str, user_record.language)

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
                cron_expression=str(cron_expression),
                callback=Fakelocation(self._api, session, location, recipient).execute,
                callback_timeout=cron_timeout,
            )
        else:
            cron = None

        user = User(cron, location, session, recipient, language)
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
