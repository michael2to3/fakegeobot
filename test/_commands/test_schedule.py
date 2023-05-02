import asynctest
from unittest.mock import MagicMock, AsyncMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from bot._commands import Schedule
from bot._config import Config
from bot.model import Geolocation


class TestSchedule(asynctest.TestCase):
    async def test_handle(self):
        bot = MagicMock()
        message_mock = MagicMock(chat_id=1, text="/schedule * * * * *")
        message_mock.reply_text = AsyncMock()
        update = Update(update_id=1, message=message_mock)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch("bot._commands.schedule.Config") as MockConfig:
            config = MagicMock(spec=Config)
            config.location = Geolocation(100, 100, 100)
            config.recipient = "fake_recipient"
            config.cron_expression = "*/5 * * * *"
            config.cron_timeout = 300
            MockConfig.return_value = config
            handler = Schedule(bot)

        with patch("bot._commands.Schedule.handle") as mock_handle:
            await handler.handle(update, context)
            mock_handle.assert_called()


if __name__ == "__main__":
    asynctest.main()
