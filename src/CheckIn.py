from telethon.sync import TelegramClient

import Geolocation
import UserAuth


class CheckIn:
    _to_username = '@poly_chess_bot'
    _client: TelegramClient
    _api_id: int
    _api_hash: str
    _union_session_name: str

    def set_to_username(self, to_username: str) -> None:
        self._to_username = to_username

    def auth_client(self, phone: str, authcode: str):
        client = UserAuth(self._union_session_name,
                          self._api_id, self._api_hash)
        client.start(phone, authcode)

    async def send_live_location(self):
        geo = Geolocation()
        await self._client.send_message(
            self._to_username,
            file=geo.get())
