from typing import Dict

from aiocron import Cron

from arg import Arg
from checkin import CheckIn
from proxytelegram import ProxyTelegram
from session import Session
from user import User
import logging


class WrapperUser:
    _user: User
    _cron: Cron

    def __init__(self, user: User, cron: Cron):
        self._user = user
        self._cron = cron


class HandlerUsers:
    logger: logging.Logger
    _users: Dict[int, WrapperUser]
    _checkin: CheckIn
    _session: Session
    _parse: Arg

    def __init__(self, path_db: str, name_db: str):
        self._users = {}
        self._checkin = CheckIn()
        self._session = Session(path_db, name_db)
        self._parse = Arg()
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        for user in self._users.values():
            self._session.save(user._user)

    def change_auth_code(self, chat_id: int, text: str):
        code = self._parse.get_auth_code(text)
        self._users[chat_id]._user._info._auth_code = code
        self._session.save(self._users[chat_id]._user)

    def change_phone_code_hash(self, chat_id: int, text: str):
        self._users[chat_id]._user._info._phone_code_hash = text

    def change_phone(self, chat_id: int, text: str):
        phone = self._parse.get_phone(text)
        self._users[chat_id]._user._info._phone = phone

    def change_schedule(self, chat_id: int, text: str):
        user = self._users[chat_id]
        schedule = self._parse.get_cron(text)
        cron = user._cron
        if cron:
            cron.stop()
        user._user._info._schedule = schedule
        cron = self._checkin.run(user._user)
        user._cron = cron

        self._users[chat_id] = user

    async def checkin(self, chat_id: int):
        if self.check_exist(chat_id):
            user = self._users[chat_id]._user
            await self._checkin.send_live_location(user)
        else:
            raise ValueError('User not exist')

    def change_user(self, user: User):
        chat_id = user._info._chat_id

        if self.check_exist(chat_id):
            self._users[chat_id]._cron.stop()
            self._users[chat_id]._user = user
        else:
            pass_cron = self._checkin.pass_cron()
            self._users[chat_id] = WrapperUser(user, pass_cron)

    def save(self, chat_id: int):
        if chat_id not in self._users:
            raise ValueError('User is not found')

        user = self._users[chat_id]._user
        self._session.save(user)

    async def require_code(self, chat_id: int) -> str:
        user = self._users[chat_id]._user
        phone = self._users[chat_id]._user._info._phone
        client = ProxyTelegram.get_client(user)
        await client.connect()
        req = await client.send_code_request(phone)
        phone_code_hash = req.phone_code_hash
        return phone_code_hash

    def start_cron(self, chat_id: int):
        user = self._users[chat_id]._user
        self._users[chat_id]._cron = self._checkin.run(user)

    async def delete(self, chat_id: int):
        try:
            self.disable(chat_id)
        except Exception as e:
            self.logger.error(str(e))

        user = self._users[chat_id]._user
        client = ProxyTelegram.get_client(user)
        try:
            await client.log_out()
        except Exception as e:
            self.logger.error(str(e))

        self._session.delete(chat_id)
        del self._users[chat_id]

    def enable(self, chat_id: int):
        self._users[chat_id]._user._info._active = True
        self._users[chat_id]._cron.start()
        self._session.save(self._users[chat_id]._user)

    def disable(self, chat_id: int):
        self._users[chat_id]._user._info._active = False
        self._users[chat_id]._cron.stop()
        self._session.save(self._users[chat_id]._user)

    def restore(self):
        users = list(self._session.load_all())

        def generate_wrap(user):
            pass_cron = self._checkin.pass_cron()
            wrap = WrapperUser(user, pass_cron)
            return wrap

        self._users = dict([(i._info._chat_id, generate_wrap(i))
                            for i in users if i._active])
        self.logger.debug(f'Start restore session. Total users: {len(users)}')
        for user in users:
            if user._active:
                chat_id = user._info._chat_id
                sid = str(chat_id)
                self.logger.debug('Acivate cron for user ' + sid)
                user = self._users[chat_id]

                user._cron = self._checkin.run(user._user)
                self._users[chat_id] = user

    def check_exist(self, chat_id: int):
        return chat_id in self._users

    def get_user(self, chat_id: int):
        return self._users[chat_id]._user
