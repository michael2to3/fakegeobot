from telethon import TelegramClient


class User:
    _session_name: str
    _username: str
    _chat_id: int
    _phone: str
    _auth_code: int
    _client: TelegramClient

    def __init__(self, session_name: str, username: str, chat_id: int,
                 phone: str, auth_code: int, client: TelegramClient):
        self._session_name = session_name
        self._username = username
        self._chat_id = chat_id
        self._phone = phone
        self._auth_code = auth_code
        self._client = client

    def __getattr__(self, name: str):
        return self.__dict__[f'{name}']

    def __setattr__(self, name: str, value):
        self.__dict__[f'{name}'] = value
