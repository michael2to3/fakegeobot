import sqlite3

from telethon import TelegramClient
from type import Api
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _client: TelegramClient
    _path_db: str

    def __init__(self,
                 api: Api,
                 info: UserInfo,
                 client: TelegramClient,
                 path_db: str = 'user.db'):
        self._api = api
        self._info = info
        self._client = client
        self._path_db = path_db

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value

    def save(self):
        conn = sqlite3.connect(self._path_db)
        c = conn.cursor()
        api = self._api
        info = self._info
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                api_id TEXT,
                api_hash TEXT,
                session_name TEXT,
                username TEXT,
                chat_id INTEGER,
                phone TEXT,
                auth_code INTEGER,
                schedule TEXT
                ):
            )
        ''')
        c.execute('''
            INSERT INTO users (
                api_id,
                api_hash,
                session_name,
                username,
                chat_id,
                phone,
                auth_code,
                schedule
 )
            VALUES (?,?,?,?,?,?,?)
        ''', (
            api._api_id,
            api._api_hash,
            info._session_name,
            info._username,
            info._chat_id,
            info._phone,
            info._auth_code,
            info._schedule
        ))
        conn.commit()
        conn.close()

    @classmethod
    def loadAll(cls, path_db: str):
        conn = sqlite3.connect(path_db)
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        rows = c.fetchall()
        conn.close()

        for row in rows:
            yield cls._generate(row, path_db)

    @classmethod
    def load(cls, chat_id: int, path_db: str):
        id = str(chat_id)
        conn = sqlite3.connect(path_db)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE chat_id=?', (id))
        row = c.fetchone()
        conn.close()

        return cls._generate(row, path_db)

    @classmethod
    def _generate(cls, row, path_db: str):
        (api_id,
         api_hash,
         session_name,
         username,
         chat_id,
         phone,
         auth_code,
         schedule) = row
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
        return cls(api, user_info, client, path_db)
