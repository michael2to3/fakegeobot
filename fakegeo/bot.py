import asyncio
from typing import Dict, List

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from telethon import TelegramClient
from telethon.errors import FloodWaitError

from arg import Arg
from checkin import CheckIn
from session import Session
from session_name import SessionName
from type import Api, UserInfo
from user import User


class Bot:
    _api_id: int
    _api_hash: str
    _app: Application
    _session: Session
    _users: Dict[int, User]
    _checkin: CheckIn

    def __init__(self,
                 token: str,
                 api_id: int,
                 api_hash: str,
                 path_db: str = 'user.db'):
        self._app = Application.builder().token(token).build()
        self._api_id = api_id
        self._api_hash = api_hash

        self._session = Session(path_db).connection().cursor().createTable()
        users = list(self._session.loadAll())
        self._users = dict([(i.chat_id, i) for i in users])

        self._checkin = CheckIn()
        for user in self._users.values():
            self._checkin.run(user)

    async def _start_schedule(self, users: List[User]):
        for user in self._users.values():
            print(user)
            await self._checkin.run(user)

    def __del__(self):
        for user in self._users.values():
            self._session.save(user)

    async def _start(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user is None:
            raise RuntimeError('User is none')

        await update.message.reply_text(
            '''
Hi comrade.\n
How to enable this future? Follow the steps:
1) Press /auth {YOUR PHONE NUMBER}
(for ex: /auth +79992132533)
2) Then you need put /code {CODE}
(fox ex: 28204)
3) if the schedule has changed, u can change the recurrence of sending messages
/schedule {CRON LANG} (for ex: /schedule 30 18 * * 5)
It's little hard, site can help you: https://cron.help/
More info: https://github.com/michael2to3/fakegeo-polychessbot
'''
        )

    async def _help(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        message = '''
/start - Start bot
/help - Show this message
/auth PHONE_NUMBER - Replace PHONE_NUMBER to your phone for auth in tg
    ex: /auth +79992132533
/code CODE - Replace CODE to your code after make auth
    ex: /code 28204
/schedule CRON - Replace CRON to your schedule to make repeat for your schedule
    ex: /schedule 30 18 * * 5
/send - Send now your fake geolocation
    ex: /send
/delete - Delete your token and all data about you
    ex: /delete
Service for help cron: https://cron.help/#30_18_*_*_5
More info: https://github.com/michael2to3/fakegeo-polychessbot
'''
        await update.message.reply_text(message)

    async def _auth(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        username = update.message.from_user.full_name
        session_name = SessionName().get_session_name()

        text = update.message.text
        phone: str
        try:
            phone = Arg().get_phone(text)
        except ValueError:
            await self._help(update, _)
            return

        client = TelegramClient(session_name, self._api_id, self._api_hash)
        emess = 'Nothing to do'
        try:
            await client.connect()
            await client.send_code_request(phone, force_sms=True)

            api = Api(self._api_id, self._api_hash)
            info = UserInfo(session_name, username, chat_id, phone, -1)
            self._users[chat_id] = User(api, info, client)
            emess = 'Can you send me your auth code'
        except RuntimeError:
            emess = 'Oops bad try access your account'
        except FloodWaitError as e:
            emess = f'Oops flood exception! Wait: {e.seconds} seconds'
        finally:
            await update.message.reply_text(emess)

    async def _send_now(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        client = self._users[chat_id]._client
        await self._checkin.send_live_location(client)
        await update.message.reply_text('Well done')

    async def _delete(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        pass

    async def _schedule(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        id = update.message.chat_id
        text = update.message.text
        if id in self._users:
            self._users[id]._info._schedule = text
            self._users[id].save()
        else:
            await update.message.reply_text('Need complete first step /auth')

    async def _raw_code(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        code: int = -1
        try:
            code = Arg().get_auth_code(text)
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

        chat_id = update.message.chat_id
        try:
            self._users[chat_id].code = code
            self._session.save(self._users[chat_id])
        except KeyError:
            emess = 'User not found, need first step /auth after send code'
            await update.message.reply_text(emess)

    async def _disable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id in self._users:
            self._users[chat_id]._active = False
            self._session.save(self._users[chat_id])
            await update.message.reply_text('Your account is disable')
        else:
            await self._start(update, _)

    async def _enable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id in self._users:
            self._users[chat_id]._active = True
            self._session.save(self._users[chat_id])
            await update.message.reply_text('Your account is enable!')
        else:
            await self._start(update, _)

    def run(self) -> None:
        app = self._app
        app.add_handler(CommandHandler('start', self._start))
        app.add_handler(CommandHandler('help', self._help))
        app.add_handler(CommandHandler('auth', self._auth))
        app.add_handler(CommandHandler('code', self._raw_code))
        app.add_handler(CommandHandler('schedule', self._schedule))
        app.add_handler(CommandHandler('send', self._send_now))
        app.add_handler(CommandHandler('disable', self._disable))
        app.add_handler(CommandHandler('enable', self._enable))
        app.add_handler(CommandHandler('delete', self._delete))

        app.run_polling()
