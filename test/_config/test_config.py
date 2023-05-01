import os
import unittest
from bot._config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        os.environ["API_ID"] = "12345"
        os.environ["API_HASH"] = "abcdefgh12345678"
        os.environ["BOT_TOKEN"] = "bot_token"
        os.environ["SQLITE_PATH"] = "sqlite_path"
        os.environ["SQLITE_NAME"] = "sqlite_name"
        os.environ["CRON_TIMEOUT"] = "600"
        os.environ["LOCATION_INTERVAL"] = "60"

    def test_config_initialization(self):
        config = Config()

        self.assertEqual(config.api.id, 12345)
        self.assertEqual(config.api.hash, "abcdefgh12345678")
        self.assertEqual(config.bot_token, "bot_token")
        self.assertEqual(config.db_path, "sqlite_path")
        self.assertEqual(config.db_name, "sqlite_name")
        self.assertEqual(config.cron_timeout, 600)
        self.assertEqual(config.location_interval, 60)
