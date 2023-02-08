from telethon import TelegramClient
from typing import Dict
from type import Api
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _clients:  Dict[str, TelegramClient]
    _active: bool

    def __init__(self, api: Api, info: UserInfo, active: bool):
        self._api = api
        self._info = info
        self._active = active

    @property
    def instance_telegramclient(self):
        api_id, api_hash = self._api
        api_id = int(api_id)
        api_hash = str(api_hash)
        session_name = self._info._session_name

        key = session_name
        if key not in self._clients:
            self._clients[key] = TelegramClient(
                self.name, self.api_id, self.api_hash)
        return self._clients[key]

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
