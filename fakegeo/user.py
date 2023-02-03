from telethon import TelegramClient
import sqlite3


class User:
    _session_name: str
    _username: str
    _chat_id: int
    _phone: str
    _auth_code: int
    _api_id: str
    _api_hash: str
    _client: TelegramClient
    _path_db: str

    def __init__(self,
                 api_id: str,
                 api_hash: str,
                 session_name: str,
                 username: str,
                 chat_id: int,
                 phone: str,
                 auth_code: int,
                 client: TelegramClient,
                 path_db: str = 'user.db'):
        self._api_id = api_id
        self._api_hash = api_hash
        self._session_name = session_name
        self._username = username
        self._chat_id = chat_id
        self._phone = phone
        self._auth_code = auth_code
        self._client = client
        self._path_db = path_db

    def __getattr__(self, name: str):
        return self.__dict__[f'{name}']

    def __setattr__(self, name: str, value):
        self.__dict__[f'{name}'] = value

    def save(self):
        conn = sqlite3.connect(self._path_db)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                session_name text,
                username text,
                chat_id integer,
                phone text,
                auth_code integer,
                api_id text,
                api_hash text
            )
        ''')
        c.execute('''
            INSERT INTO users (session_name,
 username,
 chat_id,
 phone,
 auth_code,
 api_id,
 api_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
                  (self._session_name,
                   self._username,
                   self._chat_id,
                   self._phone,
                   self._auth_code,
                   self._api_id,
                   self._api_hash))
        conn.commit()
        conn.close()

    @classmethod
    def load(cls, session_name: str, path_db: str):
        conn = sqlite3.connect(path_db)
        c = conn.cursor()
        c.execute('''
            SELECT * FROM users WHERE session_name=?
        ''', (session_name,))
        result = c.fetchone()
        if result:
            session_name, username, chat_id, phone, code, id, hash = result
            client = TelegramClient(session_name, id, hash)
            return cls(session_name,
                       username,
                       chat_id,
                       phone,
                       code,
                       id,
                       hash,
                       client)
        return None
