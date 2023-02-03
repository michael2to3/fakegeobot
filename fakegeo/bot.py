from typing import Dict

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from telethon import TelegramClient
from telethon.errors import FloodWaitError

from arg import Arg
from session_name import SessionName
from type import Api, UserInfo
from user import User


class Bot:
    _api_id: int
    _api_hash: str
    _app: Application
    _users: Dict[int, User] = {}

    def __init__(self, token: str, api_id: int, api_hash: str):
        self._app = Application.builder().token(token).build()
        self._api_id = api_id
        self._api_hash = api_hash

    async def _start(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user is None:
            raise RuntimeError('User is none')

        await update.message.reply_text(
            '''
Hi comrade. \n
How to enable this future? Follow the steps:
1) Press /auth {YOUR PHONE NUMBER} (for ex: /auth +79992132533)
2) Then you need put code (fox ex: 28204)
3) if the schedule has changed, u can change the recurrence of sending messages
/schedule {CRON LANG} (for ex: /schedule 30 18 * * 5)
It's little hard, site can help you: https://cron.help/
'''
        )

    async def _help(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        message = '''
/start - Start bot
/help - Show this message
/auth PHONE_NUMBER - Replace PHONE_NUMBER(for ex: +79992132533) to your phone
for auth in tg
/code CODE - Replace CODE(fox ex: 28204) to your code after make auth
/schedule CRON - Replace CRON(for ex: 30 18 * * 5) to your schedule
to make repeat for your schedule
Service for help cron: https://cron.help/#30_18_*_*_5
More info: https://github.com/michael2to3/fakegeo-polychessbot
'''
        await update.message.reply_text(message)

    async def echo(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

    async def req_user(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        mess = await update.message.reply_text('well hi')
        print(mess)

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
        except KeyError:
            emess = 'User not found, need first step /auth after send code'
            await update.message.reply_text(emess)

    def run(self) -> None:
        app = self._app
        app.add_handler(CommandHandler('start', self._start))
        app.add_handler(CommandHandler('help', self._help))
        app.add_handler(CommandHandler('auth', self._auth))
        app.add_handler(CommandHandler('code', self._raw_code))

        app.run_polling()
