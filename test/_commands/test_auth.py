import asynctest
from unittest.mock import MagicMock, patch, AsyncMock

from telegram import Update
from telegram.ext import ContextTypes

from bot._commands import Auth
from bot.model import ApiApp, User
from bot.abstract_bot import AbstractBot
from bot._db import DatabaseHandler


class TestAuth(asynctest.TestCase):
    class TestBot(AbstractBot):
        def __init__(self, api, db):
            self._api = api
            self._db = db
            self._users = {}

        def run(self):
            pass

        @property
        def users(self):
            return self._users

        @property
        def db(self):
            return self._db

        @property
        def api(self):
            return self._api

    def setUp(self):
        self.api = ApiApp(api_id=12345, api_hash="valid_api_hash")
        self.db = MagicMock(spec=DatabaseHandler)
        self.bot = TestAuth.TestBot(self.api, self.db)

    @patch("bot._config.config.config")
    @patch("bot._user.RequestCode")
    @patch("telethon.client.auth.AuthMethods.send_code_request", new_callable=AsyncMock)
    async def test_handle(self, mock_send_code_request, MockRequestCode, config_mock):
        config_mock.side_effect = lambda name: {
            "API_ID": "12345",
            "API_HASH": "valid_api_hash",
            "BOT_TOKEN": "test_bot_token",
            "DB_URI": "sqlite:///test_db.sqlite3",
            "CRON_TIMEOUT": "60",
            "CRON_EXPRESSION": "*/30 * * * *",
            "LOCATION_INTERVAL": "60",
            "LOCATION_LAT": "42.3601",
            "LOCATION_LONG": "71.0589",
            "RECIPIENT": "test_recipient",
        }[name]

        update = MagicMock(spec=Update)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        auth = Auth(self.bot)

        update.message.chat_id = 1
        update.message.from_user.full_name = "Test User"
        update.message.text = "/auth +123456789"
        update.message.reply_text = AsyncMock()

        MockRequestCode.get.return_value = "phone_code_hash"
        mock_send_code_request.return_value = MagicMock()

        await auth.handle(update, context)

        self.assertIn(1, self.bot.users)
        self.assertIsInstance(self.bot.users[1], User)

        self.bot.db.save_user.assert_called_once()

        update.message.reply_text.assert_called()
