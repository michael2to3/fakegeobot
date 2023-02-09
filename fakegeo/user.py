from type import Api
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _active: bool

    def __init__(self, api: Api, info: UserInfo, active: bool):
        self._api = api
        self._info = info
        self._active = active

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
