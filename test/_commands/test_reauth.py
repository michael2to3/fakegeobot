import asynctest
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asynctest
from unittest.mock import MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from bot._commands import Schedule, Info, Location, Reauth, Recipient, Send, Start


class TestReauth(asynctest.TestCase):
    async def test_handle(self):
        bot = MagicMock()
        message_mock = MagicMock(chat_id=1)
        message_mock.reply_text = AsyncMock()
        update = Update(update_id=1, message=message_mock)
        handler = Reauth(bot)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch("bot._commands.Reauth.handle") as mock_handle:
            await handler.handle(update, context)
            mock_handle.assert_called()
