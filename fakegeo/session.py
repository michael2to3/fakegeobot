import logging
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterable

from telethon import TelegramClient

from type import Api, UserInfo
from user import User


class Session:
    logger: logging.Logger
    _path_db: str
    _connect: Connection
    _cursor: Cursor

    def __init__(self, path_db: str):
        self.logger = logging.getLogger(__name__)
        self._path_db = path_db

    def connection(self):
        self._connect = sqlite3.connect(self._path_db)
        return self

    def close(self):
        self._connect.close()
        return self

    def cursor(self):
        self._cursor = self._connect.cursor()
        return self

    def createTable(self):
        self.logger.debug('Create table')
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                api_id TEXT,
                api_hash TEXT,
                session_name TEXT,
                username TEXT,
                chat_id INTEGER,
                phone TEXT,
                auth_code INTEGER,
                schedule TEXT,
                active BOOLEAN
                )
        ''')
        return self

    def commit(self):
        self._connect.commit()
        return self

    def _insert(self, user: User):
        self.logger.debug('Create user', str(user))
        api = user._api
        info = user._info
        active = user._active
        self._cursor.execute('''
            INSERT INTO users (
                api_id,
                api_hash,
                session_name,
                username,
                chat_id,
                phone,
                auth_code,
                schedule,
                active
 )
            VALUES (?,?,?,?,?,?,?,?)
        ''', (
            api._api_id,
            api._api_hash,
            info._session_name,
            info._username,
            info._chat_id,
            info._phone,
            info._auth_code,
            info._schedule,
            active
        ))

    def _update(self, user: User):
        self.logger.debug('Update user data', str(user))
        api = user._api
        info = user._info
        active = user._active
        self._cursor.execute('''
            UPDATE users SET
                api_id=?,
                api_hash=?,
                session_name=?,
                username=?,
                chat_id=?,
                phone=?,
                auth_code=?,
                schedule=?,
                active=?
            WHERE chat_id=?
        ''', (
            api._api_id,
            api._api_hash,
            info._session_name,
            info._username,
            info._phone,
            info._auth_code,
            info._schedule,
            info._chat_id,
            active
        ))

    def save(self, user: User):
        chat_id = user._info._chat_id
        current = self.load(chat_id)

        if current is None:
            self._insert(user)
        else:
            self._update(user)

        return self

    def delete(self, chat_id: int):
        self.logger.debug('Remove user ', str(chat_id))
        id = str(chat_id)
        self._cursor.execute('DELETE FROM users WHERE chat_id=?', (id))

    def loadAll(self) -> Iterable[User]:
        self.logger.debug('Load add users')
        self._cursor.execute('SELECT * FROM users')
        rows = self._cursor.fetchall()
        for row in rows:
            yield self._generate(row)

    def load(self, chat_id: int) -> User:
        self.logger.debug('Load user with chat_id ', str(chat_id))
        id = str(chat_id)
        self._cursor.execute('SELECT * FROM users WHERE chat_id=?', (id))
        row = self._cursor.fetchone()

        return self._generate(row)

    def _generate(self, row) -> User:
        (api_id,
         api_hash,
         session_name,
         username,
         chat_id,
         phone,
         auth_code,
         schedule,
         active) = row
        client = TelegramClient(
            session=session_name,
            api_id=api_id,
            api_hash=api_hash)
        user_info = UserInfo(
            session_name,
            username,
            int(chat_id),
            phone,
            auth_code,
            schedule
        )
        api = Api(api_id, api_hash)
        return User(api, user_info, client, active, self._path_db)
