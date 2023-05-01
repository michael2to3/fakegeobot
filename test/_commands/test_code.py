import asynctest
from unittest.mock import MagicMock, AsyncMock, patch

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Code
from bot._cron import Cron
from bot.model import ApiApp, User, Geolocation
from bot._db import DatabaseHandler
from bot.bot import Bot
from croniter import CroniterBadCronError
from bot._config import Config


class TestCode(asynctest.TestCase):
    def setUp(self):
        self.api = MagicMock(spec=ApiApp)
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = MagicMock(spec=Bot)
        self.bot.users = self.create_mock_users()

    def create_mock_users(self):
        users = {}
        for i in range(1, 6):
            user = MagicMock(spec=User)
            user.session.chat_id = i
            user.cron = MagicMock(spec=Cron)
            user.cron.expression = "*/5 * * * *"
            user.cron.timeout = 300
            users[i] = user
        return users

    async def test_handle(self):
        try:
            update = MagicMock(spec=Update)
            context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

            with patch("bot._commands.code.Config") as MockConfig:
                config = MagicMock(spec=Config)
                config.location = Geolocation(100, 100, 100)
                config.recipient = "fake_recipient"
                config.cron_expression = "*/5 * * * *"
                config.cron_timeout = 300
                MockConfig.return_value = config
                MockConfig.return_value.api = self.api
                code_command = Code(self.bot)

            update.message.chat_id = 1
            update.message.text = "/code 1.2.3.4.5"
            update.message.reply_text = AsyncMock()

            self.bot.db.save_user = MagicMock()

            await code_command.handle(update, context)

            code_command._get_cron(self.bot.users[1]).stop()
            update.message.reply_text.assert_called()
        except CroniterBadCronError as e:
            self.fail(f"CroniterBadCronError raised: {e}")


if __name__ == "__main__":
    asynctest.main()
