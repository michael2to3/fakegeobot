import logging
from telethon import TelegramClient
from telethon.types import InputMediaGeoLive
from model import User
from _action import Action
from model import ApiApp


class Fakelocation(Action):
    logger: logging.Logger
    _api: ApiApp
    _user: User

    def __init__(self, api: ApiApp, user: User):
        self.logger = logging.getLogger(__name__)
        self._api = api
        self._user = user

    async def execute(self):
        client = TelegramClient(
            self._user.session.session_name, self._api.id, self._api.hash
        )
        await client.connect()
        await client.sign_in(
            self._user.session.phone,
            self._user.session.auth_code,
            phone_code_hash=self._user.session.phone_code_hash,
        )

        geo = self._user.location
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get_input_media_geo_live()
        await client.send_message(self._user.recipient, file=stream)
