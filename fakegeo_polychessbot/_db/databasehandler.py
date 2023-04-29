import logging
from typing import Iterable, Optional, cast

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from _user import User, Session
from _type import Geolocation
from _cron import Cron

Base = declarative_base()


class UserRecord(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    cron_expression = Column(String)
    location = Column(String)
    session_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)
    phone = Column(String)
    auth_code = Column(Integer)
    schedule = Column(String)
    recipient = Column(String)
    phone_code_hash = Column(String)


class DatabaseHandler:
    logger: logging.Logger
    _name_db: str
    _path_db: str
    engine = None
    SessionLocal = None

    def __init__(self, path_db: str, name_db: str):
        self.logger = logging.getLogger(__name__)
        self._name_db = name_db
        self._path_db = path_db + "/" + self._name_db
        self.engine = create_engine(f"sqlite:///{self._path_db}")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def save_user(self, user: User):
        db_session = self._get_session()
        user_record = UserRecord(
            cron_expression=user.cron.cron_expression,
            location=user.location.to_json(),
            session_name=user.session.session_name,
            username=user.session.username,
            chat_id=user.session.chat_id,
            phone=user.session.phone,
            auth_code=user.session.auth_code,
            schedule=user.session.schedule,
            recipient=user.recipient,
            phone_code_hash=user.session.phone_code_hash,
        )
        db_session.add(user_record)
        db_session.commit()

    def delete_user(self, chat_id: int):
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        if user_record:
            db_session.delete(user_record)
            db_session.commit()

    def load_all_users(self) -> Iterable[User]:
        db_session = self._get_session()
        users = db_session.query(UserRecord).all()
        for user_record in users:
            user = self._user_from_record(user_record)
            if user:
                yield user

    def load_user(self, chat_id: int) -> Optional[User]:
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        if user_record:
            return self._user_from_record(user_record)
        else:
            raise ValueError("User not found")

    def user_exists(self, chat_id: int) -> bool:
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        return user_record is not None

    def _user_from_record(self, user_record: UserRecord) -> User:
        chat_id = cast(Optional[int], user_record.chat_id)
        auth_code = cast(Optional[int], user_record.auth_code)

        if chat_id is None or auth_code is None:
            raise ValueError("User not found")

        session = Session(
            str(user_record.session_name),
            str(user_record.username),
            chat_id,
            str(user_record.phone),
            auth_code,
            str(user_record.schedule),
            str(user_record.phone_code_hash),
        )

        cron = Cron(cron_expression=user_record.cron_expression, callback=None)

        location_str = str(user_record.location)
        location = Geolocation.from_json(location_str)
        recipient = cast(Optional[str], user_record.recipient)
        if recipient is None:
            recipient = "@me"

        user = User(cron, location, session, recipient)
        return user

    def _get_session(self):
        if self.SessionLocal is None:
            logging.getLogger(__name__).error("DatabaseHandler is not initialized")
            raise ValueError("DatabaseHandler is not initialized")
        return self.SessionLocal()
