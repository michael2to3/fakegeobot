from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import MessageHandler, filters
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from session_name import SessionName
from user import User
from arg import Arg
from typing import Dict


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

        await update.message.reply_html(
            rf'Hi {user.mention_html()}!',
            reply_markup=ForceReply(selective=True),
        )

    async def _help(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Help!')

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
        try:
            await client.connect()
            await client.send_code_request(phone, force_sms=True)
            await update.message.reply_text("Can you send me your auth code")
            self._users[chat_id] = User(
                api_id=self._api_id,
                api_hash=self._api_hash,
                client=client,
                username=username,
                chat_id=chat_id,
                phone=phone,
                session_name=session_name,
                auth_code=-1)
        except RuntimeError:
            await self._bad_try_auth(update, _)
        except FloodWaitError as e:
            emessage = f"Oops flood exception! Wait: {e.seconds} seconds"
            await update.message.reply_text(emessage)

    async def _bad_try_auth(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        mess = "Oops bad try access your account, I don't know what doing((("
        await update.message.reply_text(mess)

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

        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self._raw_code))

        app.run_polling()
