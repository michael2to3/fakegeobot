import asynctest
from unittest.mock import MagicMock, AsyncMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from bot._commands import Schedule, Info, Location, Reauth, Recipient, Send, Start


class TestSchedule(asynctest.TestCase):
    async def test_handle(self):
        bot = MagicMock()
        message_mock = MagicMock(chat_id=1, text="/schedule * * * * *")
        message_mock.reply_text = AsyncMock()
        update = Update(update_id=1, message=message_mock)
        handler = Schedule(bot)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch("bot._commands.Schedule.handle") as mock_handle:
            await handler.handle(update, context)
            mock_handle.assert_called()
