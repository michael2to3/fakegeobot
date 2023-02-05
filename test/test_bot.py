import unittest
import asyncio
from unittest.mock import AsyncMock,  Mock

from telegram import Update

from rootpath import fakegeo

Bot = fakegeo.Bot
Config = fakegeo.Config
Api = fakegeo.type.Api
SessionName = fakegeo.SessionName

cnf = Config()
api = Api(cnf._api_id, cnf._api_hash)


async def handler(bot: Bot, update: Update, context: Mock):
    await context.bot._start(update, context)


class BotTest(unittest.TestCase):
    def generate_bot(self):
        session = SessionName().get_session_name()
        return Bot(api, cnf._bot_token,  cnf._db_path, session)

    async def test_start(self):
        bot = self.generate_bot()
        update = Mock()
        context = Mock()
        update.message.reply_text = AsyncMock(return_value=None)

        await handler(bot, update, context)

        update.message.reply_text.assert_awaited_with("You said: Hello, Bot!")
        self.assertFalse(update)


'''
    async def test_help(self):
        pass

    async def test_auth(self):
        pass

    async def test_send_now(self):
        pass

    async def test_delete(self):
        pass

    async def test_schedule(self):
        pass

    async def test_raw_code(self):
        pass

    async def test_disable(self):
        pass

    async def test_enable(self):
        pass
    '''


async def main():
    unittest.main(argv=[''], exit=False)

if __name__ == '__main__':
    asyncio.run(main())
