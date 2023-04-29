from datetime import datetime, timedelta
from telethon.types import InputMediaGeoLive

from geolocation import Geolocation
from proxytelegram import ProxyTelegram
from user import User


class FloodError(BaseException):
    message: str
    timeout: int

    def __init__(self, message: str, timeout: int):
        self.message = message
        self.timeout = timeout


class CronAction:
    @staticmethod
    def _get_time_difference(user: User):
        now = datetime.now()
        utime = user._timestamp_last_active
        diff = now - utime
        return diff

    @staticmethod
    def _has_overload_flood(user: User, timeout: int) -> bool:
        diff = CronAction._get_time_difference(user)
        return diff < timedelta(minutes=timeout)

    @staticmethod
    async def send_live_location(user: User, to_username: str) -> None:
        timeout = 10
        if CronAction._has_overload_flood(user, timeout):
            delta = CronAction._get_time_difference(user).total_seconds()
            diff = timeout - int(delta / 60)
            raise FloodError("Detect flood from location", diff)

        user._timestamp_last_active = datetime.now()
        telegram_client = TelegramClient(user)
        await telegram_client.send_live_location(to_username)


class TelegramClient:
    def __init__(self, user: User):
        self.user = user
        self.client = ProxyTelegram.get_client(user)

    async def connect(self):
        await self.client.connect()

    async def sign_in(self):
        phone_number = self.user._info._phone
        auth_code = self.user._info._auth_code
        phonr_code_hash = self.user._info._phone_code_hash
        await self.client.sign_in(
            phone_number, auth_code, phone_code_hash=phonr_code_hash
        )

    async def send_live_location(self, to_username: str) -> None:
        await self.connect()
        await self.sign_in()

        geo = Geolocation()
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get()
        await self.client.send_message(to_username, file=stream)
