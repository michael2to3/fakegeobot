from random import randint
from rootpath import fakegeo
import time
import unittest
import os
Session = fakegeo.Session
SessionName = fakegeo.SessionName
User = fakegeo.User
UserInfo = fakegeo.type.UserInfo
Api = fakegeo.type.Api

if os.path.exists('./test.db'):
    os.remove('./test.db')


class SessionTest(unittest.TestCase):
    _path_db = './db/'

    def create_session(self):
        name = SessionName().get_session_name()
        return Session(self._path_db, name)

    def make_user(self, username: str, chat_id: int) -> User:
        session_name = SessionName().get_session_name()
        info = UserInfo(
            session_name=session_name,
            username=username,
            chat_id=chat_id,
            phone='+79992132531',
            auth_code=76481,
            schedule='* * * * *'
        )
        api = Api(api_id=12345678, api_hash='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return User(api, info, True)

    def test_save_load_user(self):
        username = 'first'
        chat_id = 123456
        user = self.make_user(username, chat_id)
        session = self.create_session()
        session.save(user)

        load = session.load(chat_id)
        self.assertIsNotNone(load, 'User not found')
        self.assertEqual(load._info._username, username)

    def test_save_update_user(self):
        username = 'first'
        new_username = 'second'
        chat_id = 1928159074
        user = self.make_user(username, chat_id)
        session = self.create_session()
        session.save(user)

        user._info._username = new_username
        session.save(user)

        del user

        load = session.load(chat_id)
        self.assertEqual(load._info._username, new_username)

    def save_load_all_users(self):
        username = 'first'
        chat_id = 1928159074
        user = self.make_user(username, chat_id)

        def get_new_user(orig: User):
            new_username = 'new name'
            orig._info._username = new_username
            orig._info._chat_id += randint(1, 200)
            return orig

        other_users = [get_new_user(user) for _ in range(10)]
        session = self.create_session()
        session.save(user)
        for us in other_users:
            session.save(us)

        loads = list(session.load_all())
        self.assertGreater(len(loads), 10)
