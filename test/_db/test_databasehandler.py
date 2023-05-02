import os
import unittest
import time
from bot.model import ApiApp, Geolocation, User, Session
from sqlalchemy import Column, Integer, String, create_engine
from bot._db.databasehandler import DatabaseHandler, Base


class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db_name = "test.sqlite"
        self.api = ApiApp(1234, "abcdefgh")

        self.db_dir_name = "test_db"
        if not os.path.exists(self.db_dir_name):
            os.makedirs(self.db_dir_name)

        full_path = os.path.join(self.db_dir_name, self.db_name)
        open(full_path, "a").close()
        os.chmod(full_path, 0o777)

        self.test_database_url = "sqlite:///" + full_path
        self.engine = create_engine(self.test_database_url)
        Base.metadata.create_all(bind=self.engine)
        self.db_handler = DatabaseHandler(
            api=self.api,
            uri="sqlite:///" + full_path,
        )

        self.sample_user = User(
            cron=None,
            location=Geolocation(50.0, 30.0, -1),
            session=Session(
                "test_session", "test_user", 123, "+1234567890", 1111, "abcd1234"
            ),
            recipient="test_recipient",
        )

    def tearDown(self):
        os.remove(os.path.join(self.db_dir_name, self.db_name))

    def test_save_and_load_user(self):
        self.db_handler.save_user(self.sample_user)
        loaded_user = self.db_handler.load_user(123)
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.session.username, "test_user")
        self.assertEqual(loaded_user.session.chat_id, 123)
        self.assertEqual(loaded_user.session.phone, "+1234567890")
        self.assertEqual(loaded_user.session.auth_code, 1111)
        self.assertEqual(loaded_user.session.phone_code_hash, "abcd1234")
        self.assertEqual(loaded_user.recipient, "test_recipient")
        self.assertEqual(loaded_user.location.lat, 50.0)
        self.assertEqual(loaded_user.location.long, 30.0)

    def test_delete_user(self):
        self.db_handler.save_user(self.sample_user)
        self.assertTrue(self.db_handler.user_exists(123))
        self.db_handler.delete_user(123)
        self.assertFalse(self.db_handler.user_exists(123))

    def test_load_all_users(self):
        self.db_handler.save_user(self.sample_user)
        users = list(self.db_handler.load_all_users())
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].session.username, "test_user")
        self.assertEqual(users[0].session.chat_id, 123)
        self.assertEqual(users[0].session.phone, "+1234567890")
        self.assertEqual(users[0].session.auth_code, 1111)
        self.assertEqual(users[0].session.phone_code_hash, "abcd1234")
        self.assertEqual(users[0].recipient, "test_recipient")
        self.assertEqual(users[0].location.lat, 50.0)
        self.assertEqual(users[0].location.long, 30.0)
