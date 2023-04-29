from typing import Dict
from aiocron import Cron
from arghelper import ArgHelper
from checkin import CheckIn
from proxytelegram import ProxyTelegram
from databasehandler import DatabaseHandler
from user import User
import logging


class UserWrapper:
    _user: User
    _cron: Cron

    def __init__(self, user: User, cron: Cron):
        self._user = user
        self._cron = cron


class UserManager:
    logger: logging.Logger
    _users: Dict[int, UserWrapper]
    _checkin: CheckIn
    _session: DatabaseHandler
    _parse: ArgHelper

    def __init__(self, path_db: str, name_db: str):
        self._users = {}
        self._checkin = CheckIn()
        self._session = DatabaseHandler(path_db, name_db)
        self._parse = ArgHelper()
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        for user in self._users.values():
            self._session.save(user._user)

    def update_auth_code(self, chat_id: int, text: str) -> None:
        if self._session is None:
            return

        code = self._parse.get_auth_code(text)
        self._users[chat_id]._user._info._auth_code = code
        self._session.save(self._users[chat_id]._user)

    def update_phone_code_hash(self, chat_id: int, text: str) -> None:
        self._users[chat_id]._user._info._phone_code_hash = text

    def update_phone(self, chat_id: int, text: str) -> None:
        phone = self._parse.get_phone(text)
        self._users[chat_id]._user._info._phone = phone

    def update_schedule(self, chat_id: int, text: str) -> None:
        user_wrapper = self._users[chat_id]
        schedule = self._parse.get_cron(text)
        cron = user_wrapper._cron
        if cron:
            cron.stop()
        user_wrapper._user._info._schedule = schedule
        cron = self._checkin.run(user_wrapper._user)
        user_wrapper._cron = cron

        self._users[chat_id] = user_wrapper
        self.save(chat_id)

    async def perform_checkin(self, chat_id: int) -> None:
        if self.check_exist(chat_id):
            user = self._users[chat_id]._user
            await self._checkin.send_live_location(user)
        else:
            raise ValueError("User not exist")

    def update_user(self, user: User) -> None:
        chat_id = user._info._chat_id

        if self.check_exist(chat_id):
            self._users[chat_id]._cron.stop()
            self._users[chat_id]._user = user
        else:
            pass_cron = self._checkin.pass_cron()
            self._users[chat_id] = UserWrapper(user, pass_cron)

    def save(self, chat_id: int) -> None:
        if chat_id not in self._users:
            raise ValueError("User is not found")

        user = self._users[chat_id]._user
        self._session.save(user)

    async def request_code(self, chat_id: int) -> str:
        user = self._users[chat_id]._user
        phone = self._users[chat_id]._user._info._phone
        client = ProxyTelegram.get_client(user)
        await client.connect()
        req = await client.send_code_request(phone)
        phone_code_hash = req.phone_code_hash
        return phone_code_hash

    def start_cron(self, chat_id: int) -> None:
        user = self._users[chat_id]._user
        self._users[chat_id]._cron = self._checkin.run(user)

    async def delete(self, chat_id: int) -> None:
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

    def enable(self, chat_id: int) -> None:
        if self._users[chat_id]._user._info is None:
            raise ValueError("User is not found")

        self._users[chat_id]._cron.start()
        self.save(chat_id)

    def disable(self, chat_id: int) -> None:
        self._users[chat_id]._cron.stop()
        self.save(chat_id)

    def restore(self) -> None:
        users = list(self._session.load_all())

        def generate_wrap(user: User) -> UserWrapper:
            pass_cron = self._checkin.pass_cron()
            wrap = UserWrapper(user, pass_cron)
            return wrap

        self._users = dict(
            [(i._info._chat_id, generate_wrap(i)) for i in users if i._active]
        )
        self.logger.debug(f"Start restore session. Total users: {len(users)}")
        for user in users:
            if user._active:
                chat_id = user._info._chat_id
                sid = str(chat_id)
                self.logger.debug("Acivate cron for user " + sid)
                user_wrapper = self._users[chat_id]

                user_wrapper._cron = self._checkin.run(user_wrapper._user)
                self._users[chat_id] = user_wrapper

    def check_exist(self, chat_id: int) -> bool:
        return chat_id in self._users

    def get_user(self, chat_id: int) -> User:
        return self._users[chat_id]._user
