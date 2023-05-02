from .._cron import Cron
from .geolocation import Geolocation
from .session import Session


class User:
    __slots__ = ("_cron", "_location", "_session", "_recipient")

    def __init__(
        self,
        cron: Cron | None,
        location: Geolocation | None,
        session: Session,
        recipient: str | None,
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

    def __str__(self):
        return f"User(cron={self.cron}, location={self.location}, session={self.session}, recipient={self.recipient})"
