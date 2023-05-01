import asynctest
from unittest.mock import MagicMock, AsyncMock

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Delete
from bot.model import ApiApp, User
from bot._db import DatabaseHandler
from bot.bot import Bot


class TestDelete(asynctest.TestCase):
    def setUp(self):
        self.api = MagicMock(spec=ApiApp)
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = Bot(self.api, self.token, self.db)

    async def test_handle(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        delete_command = Delete(self.bot)

        update.message.chat_id = 1
        update.message.reply_text = AsyncMock()

        self.bot.users[1] = MagicMock(spec=User)
        self.bot.db.delete_user = MagicMock()

        await delete_command.handle(update, context)

        update.message.reply_text.assert_called()
