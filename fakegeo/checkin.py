import logging

from aiocron import crontab
from telethon.sync import TelegramClient
from telethon.types import InputMediaGeoLive

from geolocation import Geolocation
from user import User


class CheckIn:
    logger: logging.Logger
    _to_username = '@poly_chess_bot'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def send_live_location(self, user: User) -> None:

        client = user.instance_telegramclient
        phone_number = user._info._phone
        auth_code = user._info._auth_code

        await client.connect()
        client.start(phone_number, code_callback=lambda: auth_code)

        geo = Geolocation()
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get()
        await client.send_message(
            self._to_username,
            file=stream)

    def run(self, user: User):
        cron: str = user._info._schedule
        def func(): return self.send_live_location(user)
        return crontab(cron, func=func, start=True)

    def pass_cron(self):
        schedule = '30 18 * * 6'

        def func():
            pass
        return crontab(schedule, func=func, start=False)
