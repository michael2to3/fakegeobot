
from telethon.types import InputMediaGeoLive
from proxytelegram import ProxyTelegram

from geolocation import Geolocation
from user import User


class CronAction:
    @staticmethod
    async def send_live_location(user: User, to_username: str) -> None:
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
