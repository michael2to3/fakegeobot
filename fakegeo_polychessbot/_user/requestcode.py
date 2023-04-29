from _type import User, ApiApp
from telethon import TelegramClient


class RequestCode:
    @staticmethod
    async def get(user: User, api: ApiApp) -> str:
        phone = user.session.phone
        client = TelegramClient(user.session.session_name, api.id, api.hash)
        await client.connect()
        req = await client.send_code_request(phone)
        phone_code_hash = req.phone_code_hash
        return phone_code_hash
