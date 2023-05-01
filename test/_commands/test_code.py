import asynctest
from unittest.mock import MagicMock, AsyncMock

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Code
from bot._cron import Cron
from bot.model import ApiApp, User
from bot._db import DatabaseHandler
from bot.bot import Bot
from croniter import CroniterBadCronError


class TestCode(asynctest.TestCase):
    def setUp(self):
        self.api = MagicMock(spec=ApiApp)
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = Bot(self.api, self.token, self.db)

    async def test_handle(self):
        try:
            update = MagicMock(spec=Update)
            context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
            code_command = Code(self.bot)

            update.message.chat_id = 1
            update.message.text = "/code 1.2.3.4.5"
            update.message.reply_text = AsyncMock()

            self.bot.users[1] = MagicMock(spec=User)
            mock_cron = MagicMock(spec=Cron)
            mock_cron.expression = "*/5 * * * *"
            mock_cron.timeout = 300
            self.bot.users[1].cron = mock_cron
            self.bot.db.save_user = MagicMock()

            await code_command.handle(update, context)

            update.message.reply_text.assert_called()
        except CroniterBadCronError as e:
            self.fail(f"CroniterBadCronError raised: {e}")
