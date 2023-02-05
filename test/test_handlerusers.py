import unittest
from random import randint
from rootpath import fakegeo
HandlerUsers = fakegeo.HandlerUsers
SessionName = fakegeo.SessionName
Session = fakegeo.Session
User = fakegeo.User
UserInfo = fakegeo.type.UserInfo
Api = fakegeo.type.Api


def make_user(username: str, chat_id: int) -> User:
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


def make_handler(path_db: str, name_db: str):
    return HandlerUsers(path_db, name_db)


class HandlerUsersTest(unittest.TestCase):
    _path_db = './db/'
    _name_db = SessionName().get_session_name()

    def make_user(self, username: str, chat_id: int) -> User:
        return make_user(username, chat_id)

    def make_handler(self, name_db: str | None = None):
        if name_db is None:
            name_db = self._name_db
        return make_handler(self._path_db, name_db)

    def create_session(self):
        return Session(self._path_db, self._name_db)

    def test_change_auth_code(self):
        chat_id = 123456
        new_auth_code = '/code 12345'
        format_code = 12345
        raise_auth_code = '/code 123456'
        username = 'username'

        user = self.make_user(username, chat_id)

        handler = self.make_handler()
        handler.change_user(user)
        self.assertRaises(ValueError, handler.change_auth_code,
                          chat_id, raise_auth_code)
        handler.change_auth_code(chat_id, new_auth_code)

        code = handler.get_user(chat_id)._info._auth_code
        self.assertEqual(code, format_code)

    def test_change_phone(self):
        chat_id = 123456
        new_phone = '/phone 88005553535'
        format_phone = '88005553535'
        username = 'username'

        user = self.make_user(username, chat_id)

        handler = self.make_handler()
        handler.change_user(user)
        handler.change_phone(chat_id, new_phone)

        phone = handler.get_user(chat_id)._info._phone
        self.assertEqual(phone, format_phone)

    def test_change_schedule(self):
        chat_id = 123456
        new_sch = '/schedule * * * * *'
        username = 'username'

        user = self.make_user(username, chat_id)

        handler = self.make_handler()
        handler.change_user(user)
        handler.change_schedule(chat_id, new_sch)

        sch = handler.get_user(chat_id)._info._schedule
        self.assertEqual(sch, new_sch)

    def test_checkin(self):
        pass

    def test_change_user_exists(self):
        chat_id = 123456
        username = 'username'

        user = self.make_user(username, chat_id)

        handler = self.make_handler()
        handler.change_user(user)

        new_username = 'second'
        update_user = self.make_user(new_username, chat_id)

        handler.change_user(update_user)
        load = handler.get_user(chat_id)
        self.assertEqual(load._info._username, new_username)

    def test_change_user_not_exists(self):
        chat_id = 123456
        username = 'username'
        user = self.make_user(username, chat_id)

        handler = self.make_handler()
        handler.change_user(user)

        self.assertEqual(handler.get_user(chat_id)._info._username, username)

    def test_require_code(self):
        pass

    def test_start_cron(self):
        handler = self.make_handler()
        username = 'username'
        chat_id = 665666
        user = self.make_user(username, chat_id)
        cron = handler._checkin.run(user)
        self.assertIsNotNone(cron)

    def test_enable(self):
        username = 'username'
        chat_id = 665666

        handler = self.make_handler()
        user = self.make_user(username, chat_id)

        handler.change_user(user)
        handler.enable(chat_id)

        handler.enable(chat_id)
        load = handler.get_user(chat_id)
        self.assertEqual(load._active, True)

    def test_disable(self):
        username = 'username'
        chat_id = 665666

        handler = self.make_handler()
        user = self.make_user(username, chat_id)

        handler.change_user(user)
        handler.enable(chat_id)

        handler.enable(chat_id)
        load = handler.get_user(chat_id)
        self.assertEqual(load._active, True)

    def test_restore(self):
        len = 10
        ids = [randint(0, 666666) for _ in range(len)]
        it = iter(ids)
        users = [self.make_user('same name', next(it)) for _ in range(len)]
        session_name = SessionName().get_session_name()
        handler = self.make_handler(session_name)
        for user in users:
            handler.change_user(user)

        del handler
        del users

        handler = self.make_handler(session_name)
        handler.restore()
        loads = handler._users.values()
        load_ids = [i._user._info._chat_id for i in loads]
        self.assertEqual(set(ids), set(load_ids))

    def test_check_exist(self):
        ex_id = 66892312
        nex_id = 55555555
        exist_user = self.make_user('same name', ex_id)

        handler = self.make_handler()
        handler.change_user(exist_user)

        self.assertEqual(handler.check_exist(ex_id), True)
        self.assertEqual(handler.check_exist(nex_id), False)
