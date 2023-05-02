import asynctest
from unittest.mock import MagicMock, AsyncMock

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Help
from bot.model import ApiApp
from bot._db import DatabaseHandler
from bot.bot import Bot


class TestHelp(asynctest.TestCase):
    def setUp(self):
        self.api = MagicMock(spec=ApiApp)
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = Bot(self.api, self.token, self.db)

    async def test_handle(self):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        help_command = Help(self.bot)

        update.message.reply_text = AsyncMock()

        await help_command.handle(update, context)

        update.message.reply_text.assert_called()
