import asynctest
from unittest.mock import MagicMock, AsyncMock

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Send
from bot._cron import Cron
from bot.model import ApiApp, User, Geolocation
from bot._db import DatabaseHandler
from bot.bot import Bot, BotContext
from croniter import CroniterBadCronError
from bot._config import Config
from bot.text import TextHelper
from bot._action import Fakelocation


class TestSend(asynctest.TestCase):
    def setUp(self):
        self.api = ApiApp(api_id=1, api_hash="1")
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = MagicMock(spec=Bot)
        config = MagicMock(spec=Config)
        config.location = Geolocation(100, 100, 100)
        config.recipient = "fake_recipient"
        config.cron_expression = "*/5 * * * *"
        config.cron_timeout = 300
        self.bot.context = BotContext(self.api, {}, self.db, config)
        self.update = MagicMock(spec=Update)
        self.text_helper = MagicMock(spec=TextHelper)
        self.bot.users = self.create_mock_users()
        self.bot.context.users = self.bot.users

    def create_mock_users(self):
        users = {}
        for i in range(1, 6):
            user = MagicMock(spec=User)
            user.session.chat_id = i
            user.cron = MagicMock(spec=Cron)
            user.cron.stop = MagicMock()
            user.cron.start = MagicMock()
            user.cron.expression = "*/5 * * * *"
            user.cron.timeout = 300
            user.location = Geolocation(0, 0, 0)
            user.recipient = "fake_recipient"
            users[i] = user
        return users

    async def test_handle(self):
        try:
            update = MagicMock(spec=Update)
            context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

            send_command = Send(self.bot.context, self.text_helper)

            update.message.location = None
            update.message.chat_id = 1
            update.message.text = "/send"
            update.message.reply_text = AsyncMock()

            self.bot.db.save_user = MagicMock()

            # Mock Fakelocation
            with asynctest.patch.object(
                Fakelocation, "execute", new_callable=AsyncMock
            ) as mock_fakelocation:
                await send_command.handle(update, context)

            update.message.reply_text.assert_called()

            update.message.reply_text.reset_mock()
            self.bot.context.users[1].cron.stop()
        except CroniterBadCronError as e:
            self.fail(f"CroniterBadCronError raised: {e}")
