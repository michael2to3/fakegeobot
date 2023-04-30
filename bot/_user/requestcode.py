from ..model import ApiApp, User
from telethon import TelegramClient


class RequestCode:
    @staticmethod
    async def get(user: User, api: ApiApp) -> str:
        phone = user.session.phone
        if phone is None:
            raise ValueError("Please enter your phone number")

        client = TelegramClient(user.session.session_name, api.id, api.hash)
        await client.connect()

        req = await client.send_code_request(phone)
        phone_code_hash = req.phone_code_hash
        return phone_code_hash
