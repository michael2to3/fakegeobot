from telethon.sync import TelegramClient


class UserAuth:
    _client: TelegramClient

    def __init__(self, session_name: str, api_id: int, api_hash: str):
        self._client = TelegramClient(
            session_name, api_id, api_hash)

    def start(self, phone_number: str, auth_token: str) -> None:
        self._client.start(lambda: phone_number, lambda: auth_token)

    def get_session(self) -> TelegramClient:
        return self._client
