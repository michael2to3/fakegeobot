import logging
from typing import Iterable

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from type import Api, UserInfo
from user import User

Base = declarative_base()


class UserRecord(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    api_id = Column(String)
    api_hash = Column(String)
    session_name = Column(String)
    username = Column(String)
    chat_id = Column(Integer)
    phone = Column(String)
    auth_code = Column(Integer)
    schedule = Column(String)
    active = Column(Boolean)
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

    def save(self, user: User):
        db_session = self._get_session()
        user_record = UserRecord(
            api_id=user._api._id,
            api_hash=user._api._hash,
            session_name=user._info._session_name,
            username=user._info._username,
            chat_id=user._info._chat_id,
            phone=user._info._phone,
            auth_code=user._info._auth_code,
            schedule=user._info._schedule,
            active=user._active,
            phone_code_hash=user._info._phone_code_hash,
        )
        db_session.add(user_record)
        db_session.commit()

    def delete(self, chat_id: int):
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        if user_record:
            db_session.delete(user_record)
            db_session.commit()

    def load_all(self) -> Iterable[User]:
        db_session = self._get_session()
        users = db_session.query(UserRecord).all()
        for user_record in users:
            user = self._generate(user_record)
            if user:
                yield user

    def load(self, chat_id: int) -> User:
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        if user_record:
            return self._generate(user_record)
        else:
            raise ValueError("User not found")

    def check_exist(self, chat_id: int) -> bool:
        db_session = self._get_session()
        user_record = (
            db_session.query(UserRecord).filter(UserRecord.chat_id == chat_id).first()
        )
        return user_record is not None

    def _generate(self, user_record) -> User:
        user_info = UserInfo(
            user_record.session_name,
            user_record.username,
            user_record.chat_id,
            user_record.phone,
            user_record.auth_code,
            user_record.schedule,
            user_record.phone_code_hash,
        )

        api = Api(user_record.api_id, user_record.api_hash)
        return User(api, user_info, user_record.active)

    def _get_session(self):
        if self.SessionLocal is None:
            logging.getLogger(__name__).error("DatabaseHandler is not initialized")
            raise ValueError("DatabaseHandler is not initialized")
        return self.SessionLocal()
