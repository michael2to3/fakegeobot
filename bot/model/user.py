from _cron import Cron
from model import Session
from model import Geolocation


class User:
    __slots__ = ("_cron", "_location", "_session", "_recipient")

    def __init__(
        self,
        cron: Cron,
        location: Geolocation,
        session: Session,
        recipient: str,
    ):
        self._cron = cron
        self._location = location
        self._session = session
        self._recipient = recipient

    @property
    def cron(self):
        return self._cron

    @cron.setter
    def cron(self, value):
        self._cron = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, value):
        self._recipient = value
