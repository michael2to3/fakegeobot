from telethon import TelegramClient
from user import User


class ProxyTelegram:
    @staticmethod
    def get_client(user: User) -> TelegramClient:
        session_name = user._info._session_name
        api_id = user._api._id
        api_hash = user._api._hash
        return TelegramClient(session_name, api_id, api_hash)
