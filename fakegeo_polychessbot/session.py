import logging
import sqlite3
from sqlite3 import Connection
from typing import Iterable

from type import Api, UserInfo
from user import User


class Session:
    logger: logging.Logger
    _name_db: str
    _path_db: str

    def __init__(self, path_db: str, name_db: str):
        self.logger = logging.getLogger(__name__)
        self._name_db = name_db
        self._path_db = path_db + "/" + self._name_db

        self.create_table()

    def connect(self) -> Connection:
        return sqlite3.connect(self._path_db)

    def create_table(self):
        con = self.connect()
        con.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                api_id TEXT,
                api_hash TEXT,
                session_name TEXT,
                username TEXT,
                chat_id INTEGER,
                phone TEXT,
                auth_code INTEGER,
                schedule TEXT,
                active BOOLEAN,
                phone_code_hash TEXT
                )
        """
        )
        con.commit()
        con.close()
        return self

    def _insert(self, user: User):
        api = user._api
        info = user._info
        active = user._active
        con = self.connect()
        con.cursor().execute(
            """
            INSERT INTO users (
                api_id,
                api_hash,
                session_name,
                username,
                chat_id,
                phone,
                auth_code,
                schedule,
                active,
                phone_code_hash
 )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
            (
                api._id,
                api._hash,
                info._session_name,
                info._username,
                str(info._chat_id),
                info._phone,
                info._auth_code,
                info._schedule,
                str(int(active)),
                info._phone_code_hash,
            ),
        )
        con.commit()
        con.close()
        return self

    def _update(self, user: User):
        api = user._api
        info = user._info
        active = user._active
        con = self.connect()
        con.cursor().execute(
            """
            UPDATE users SET
                api_id=?,
                api_hash=?,
                session_name=?,
                username=?,
                phone=?,
                auth_code=?,
                schedule=?,
                active=?,
                phone_code_hash=?
            WHERE chat_id=?
        """,
            (
                api._id,
                api._hash,
                info._session_name,
                info._username,
                info._phone,
                info._auth_code,
                info._schedule,
                str(int(active)),
                info._phone_code_hash,
                str(info._chat_id),
            ),
        )
        con.commit()
        con.close()

    def save(self, user: User):
        chat_id = user._info._chat_id

        if self.check_exist(chat_id):
            self._update(user)
        else:
            self._insert(user)

        return self

    def delete(self, chat_id: int):
        sid = str(chat_id)
        sql = "DELETE FROM users WHERE chat_id=?"
        con = self.connect()
        con.cursor().execute(sql, (sid,))
        con.commit()
        con.close()

    def load_all(self) -> Iterable[User]:
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        con.close()
        for row in rows:
            yield self._generate(row)

    def load(self, chat_id: int) -> User:
        id = str(chat_id)
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE chat_id=?", (id,))
        row = cursor.fetchone()
        con.close()

        return self._generate(row)

    def check_exist(self, chat_id: int) -> bool:
        id = str(chat_id)
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE chat_id=?", (id,))
        row = cursor.fetchone()
        con.close()

        return row is not None

    def _generate(self, row) -> User:
        if row is None:
            raise TypeError("Not found, row is None")

        (
            api_id,
            api_hash,
            session_name,
            username,
            chat_id,
            phone,
            auth_code,
            schedule,
            active,
            phone_code_hash,
        ) = row

        user_info = UserInfo(
            session_name,
            username,
            int(chat_id),
            phone,
            auth_code,
            schedule,
            phone_code_hash,
        )
        api = Api(api_id, api_hash)
        return User(api, user_info, active)
