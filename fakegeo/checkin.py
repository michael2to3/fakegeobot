from telethon.sync import TelegramClient
from telethon.types import InputMediaGeoLive

from geolocation import Geolocation
from userauth import UserAuth


class CheckIn:
    _to_username = '@poly_chess_bot'
    _client: TelegramClient
    _api_id: int
    _api_hash: str
    _union_session_name: str

    def set_to_username(self, to_username: str) -> None:
        self._to_username = to_username

    def auth_client(self, phone: str, authcode: str) -> None:
        client = UserAuth(self._union_session_name,
                          self._api_id, self._api_hash)
        client.start(phone, authcode)

    async def send_live_location(self) -> None:
        geo = Geolocation()
        # Well... Ignore error from library tg, it's ok
        # Still send InputMediaGeoLive
        stream: InputMediaGeoLive = geo.get()
        await self._client.send_message(
            self._to_username,
            file=stream)
