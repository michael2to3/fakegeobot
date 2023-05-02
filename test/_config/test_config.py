import unittest
from unittest.mock import patch
from bot._config.config import Config
from bot.model import ApiApp, Geolocation


class TestConfig(unittest.TestCase):
    @patch("bot._config.config.config")
    def test_config_init(self, config_mock):
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

        config = Config()

        self.assertEqual(config.api, ApiApp(12345, "valid_api_hash"))
        self.assertEqual(config.bot_token, "test_bot_token")
        self.assertEqual(config.db_uri, "sqlite:///test_db.sqlite3")
        self.assertEqual(config.cron_timeout, 60)
        self.assertEqual(config.cron_expression, "*/30 * * * *")
        self.assertEqual(config.location_interval, 60)
        self.assertEqual(config.location, Geolocation(42.3601, 71.0589, 60))
        self.assertEqual(config.recipient, "test_recipient")
