
from datetime import datetime, timedelta
from telethon.types import InputMediaGeoLive
from proxytelegram import ProxyTelegram

from geolocation import Geolocation
from user import User


class FloodError(BaseException):
    message: str
    timeout: int

    def __init__(self, message: str, timeout: int):
        self.message = message
        self.timeout = timeout


class CronAction:
    @staticmethod
    def _get_diff(user: User, timeout: int):
        now = datetime.now()
        utime = user._timestamp_last_active
        diff = now - utime
        return diff

    @staticmethod
    def _has_overload_flood(user: User, timeout: int) -> bool:
        diff = CronAction._get_diff(user, timeout)
        return diff < timedelta(minutes=timeout)

    @staticmethod
    async def send_live_location(user: User, to_username: str) -> None:
        timeout = 10
        if CronAction._has_overload_flood(user, timeout):
            delta = CronAction._get_diff(user, timeout).total_seconds()
            diff = timeout - int(delta / 60)
            raise FloodError('Detect flood from location', diff)
        user._timestamp_last_active = datetime.now()
        await CronAction._send_live_location(user, to_username)

    @staticmethod
    async def _send_live_location(user: User, to_username: str) -> None:
        phone_number = user._info._phone
        auth_code = user._info._auth_code
        hash = user._info._phone_code_hash

        client = ProxyTelegram.get_client(user)
        await client.connect()
        await client.sign_in(phone_number, auth_code, phone_code_hash=hash)

        geo = Geolocation()
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get()
        await client.send_message(
            to_username,
            file=stream)
