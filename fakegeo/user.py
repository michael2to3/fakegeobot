from telethon import TelegramClient
from type import Api
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _client: TelegramClient
    _active: bool
    _path_db: str

    def __init__(self,
                 api: Api,
                 info: UserInfo,
                 client: TelegramClient,
                 active: bool = True,
                 path_db: str = 'user.db'):
        self._api = api
        self._info = info
        self._client = client
        self._active = active
        self._path_db = path_db

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
