from telethon import TelegramClient
from type import Api
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _client:  TelegramClient | None
    _active: bool

    def __init__(self, api: Api, info: UserInfo, active: bool):
        self._api = api
        self._info = info
        self._active = active
        self._client = None

    def instance_telegramclient(self) -> TelegramClient:
        session_name = self._info._session_name
        api = self._api
        if self._client is None:
            self._client = TelegramClient(session_name, api._id, api._hash)
        return self._client

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
