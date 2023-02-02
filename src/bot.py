from telethon import events
from config import Config
from userauth import UserAuth

receiver = '@echecs95'


class Bot:
    _session_name: str = 'Bot'
    _token: str

    def __init__(self, token: str):
        config = Config()
        auth = UserAuth('bot', config.get_api_id(), config.get_api_hash())
        self._client = auth.get_session()
        self._token = token

    async def run(self):
        client = self._client
        client.start()

        entity = await client.get_entity(receiver)

        message = "Hi"
        await client.send_message(entity, message)

        @client.on(events.NewMessage(chats=receiver))
        async def handler(event):
            response = event.message.message
            print(f"Received response: {response}")

        client.run_until_disconnected()
