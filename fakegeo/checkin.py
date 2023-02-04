from telethon.sync import TelegramClient
from telethon.types import InputMediaGeoLive
from user import User
from aiocron import crontab
from geolocation import Geolocation


class CheckIn:
    _to_username = '@poly_chess_bot'

    async def send_live_location(self, user: TelegramClient) -> None:
        geo = Geolocation()
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get()
        await user.send_message(
            self._to_username,
            file=stream)

    async def run(self, user: User):
        cron: str = user._info._schedule
        def func(): return self.send_live_location(user._client)
        await func()
        crontab(cron, func=func, start=True)
