import unittest
from unittest.mock import MagicMock, patch

from telegram import Update
from telegram.ext import ContextTypes

from bot._db import DatabaseHandler
from bot.bot import Bot
from bot.model import ApiApp, Session, User


class TestBot(unittest.TestCase):
    def setUp(self):
        self.api = MagicMock(spec=ApiApp)
        self.token = "fake_token"
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = Bot(self.api, self.token, self.db)

    def test_init(self):
        self.assertIsInstance(self.bot, Bot)
        self.assertEqual(self.bot._api, self.api)
        self.assertEqual(self.bot._db, self.db)

    @patch("bot.Start")
    async def test_handle_command(self, MockStart):
        update = MagicMock(spec=Update)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        update.message.text = "/start"

        await self.bot._handle_command("start", update, context)

        MockStart.return_value.handle.assert_called_once_with(update, context)

    @patch("telegram.ext.Application.run_polling")
    def test_run(self, mock_run_polling):
        self.bot.run()

        mock_run_polling.assert_called_once()

    def test_users_property(self):
        session = Session(
            session_name="test",
            username="michael",
            chat_id=-1,
            phone="+123456789",
            auth_code=1234,
            phone_code_hash="1234",
        )
        users = {1: User(cron=None, location=None, session=session, recipient="@me")}
        self.bot._users = users

        self.assertEqual(self.bot.users, users)

    def test_db_property(self):
        self.assertEqual(self.bot.db, self.db)

    def test_api_property(self):
        self.assertEqual(self.bot.api, self.api)


if __name__ == "__main__":
    unittest.main()
