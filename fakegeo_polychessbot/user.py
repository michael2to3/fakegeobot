from type import Api
from datetime import datetime
from type import UserInfo


class User:
    _api: Api
    _info: UserInfo
    _active: bool
    _timestamp_last_active: datetime

    def __init__(self, api: Api, info: UserInfo, active: bool):
        self._api = api
        self._info = info
        self._active = active
        self._timestamp_last_active = datetime(1, 1, 1, 0, 0)

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
