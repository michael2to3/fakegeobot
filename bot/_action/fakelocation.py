import logging
from telethon import TelegramClient
from telethon.types import InputMediaGeoLive
from model import User
from _action import Action
from model import ApiApp, Session, Geolocation


class Fakelocation(Action):
    logger: logging.Logger
    _api: ApiApp
    _session: Session
    _location: Geolocation
    _recipient: str

    def __init__(
        self, api: ApiApp, session: Session, location: Geolocation, recipient: str
    ):
        self.logger = logging.getLogger(__name__)
        self._api = api
        self._session = session
        self._location = location
        self._recipient = recipient

    async def execute(self):
        if self._session.phone is None:
            raise ValueError("Please enter your phone number")
        if self._session.auth_code is None or self._session.phone_code_hash is None:
            raise ValueError("Please enter your auth code")
        if self._location is None:
            raise ValueError("Please enter your location")
        if self._recipient is None:
            raise ValueError("Please enter your recipient")

        client = TelegramClient(
            self._session.session_name, self._api.id, self._api.hash
        )
        await client.connect()
        await client.sign_in(
            self._session.phone,
            self._session.auth_code,
            phone_code_hash=self._session.phone_code_hash,
        )

        geo = self._location
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get_input_media_geo_live()
        await client.send_message(self._recipient, file=stream)
