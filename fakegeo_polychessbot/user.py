from type import Api
from datetime import datetime
from type import UserInfo


class User:
    def __init__(self, api: Api, info: UserInfo, active: bool):
        self.api = api
        self.info = info
        self.active = active
        self.timestamp_last_active = datetime(1, 1, 1, 0, 0)

    @property
    def api(self) -> Api:
        return self._api

    @api.setter
    def api(self, value: Api):
        self._api = value

    @property
    def info(self) -> UserInfo:
        return self._info

    @info.setter
    def info(self, value: UserInfo):
        self._info = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value

    @property
    def timestamp_last_active(self) -> datetime:
        return self._timestamp_last_active

    @timestamp_last_active.setter
    def timestamp_last_active(self, value: datetime):
        self._timestamp_last_active = value
