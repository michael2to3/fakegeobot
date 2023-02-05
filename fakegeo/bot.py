from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from telethon.errors import FloodWaitError

from handlerusers import HandlerUsers
from session_name import SessionName
from type import Api, UserInfo
from user import User
import logging


class Bot:
    logger: logging.Logger
    _api: Api
    _app: Application
    _users: HandlerUsers

    def __init__(self, api: Api, token: str, path_db: str, name_db: str):
        self.logger = logging.getLogger(__name__)
        self._app = Application.builder().token(token).build()
        self._api = api
        self._users = HandlerUsers(path_db, name_db).restore()

    async def _start(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Start for user', str(update))
        await update.message.reply_text(
            '''
Hi comrade.\n
How to enable this future? Follow the steps:
1) Press /auth {YOUR PHONE NUMBER}
(for ex: /auth +79992132533)
2) Then you need put /code {CODE}
(fox ex: 28204, need put 2.8.2.0.4)
3) if the schedule has changed, u can change the recurrence of sending messages
/schedule {CRON LANG} (for ex: /schedule 30 18 * * 5)
It's little hard, site can help you: https://cron.help/
More info: https://github.com/michael2to3/fakegeo-polychessbot
''')

    async def _help(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Help for user', str(update))
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
Support: https://t.me/+EGnT6v3APokxMGYy
'''
        await update.message.reply_text(message)

    async def _auth(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Auth for user', str(update))
        chat_id = update.message.chat_id

        if self._users.check_exist(chat_id):
            emess = "U already auth"
            await update.message.reply_text(emess)
            return

        username = update.message.from_user.full_name
        session_name = SessionName().get_session_name()

        text = update.message.text

        emess = 'You send code to auth. Can you put me /code {AUTHCODE}'

        schedule = '30_18_*_*_5'
        info = UserInfo(session_name, username,
                        chat_id, '', -1, schedule)
        user = User(self._api, info, True)

        try:
            self._users.change_user(user)
            self._users.change_phone(chat_id, text)
            await self._users.require_code(chat_id)

            emess = '''
Send me auth code each char separated by a dot
For example: Login code: 61516
You put: /code 6.1.5.1.6
It's need to bypass protect telegram
'''
        except RuntimeError:
            emess = 'Oops bad try access your account'
        except FloodWaitError as e:
            emess = f'Oops flood exception! Wait: {e.seconds} seconds'
        finally:
            await update.message.reply_text(emess)

    async def _send_now(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Send now for user', str(update))
        chat_id = update.message.chat_id
        await self._users.checkin(chat_id)
        await update.message.reply_text('Well done')

    async def _delete(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Delete for user', str(update))
        chat_id = update.message.chat_id
        await self._users.delete(chat_id)
        await update.message.reply_text('Your account was deleted!')

    async def _schedule(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        self.logger.debug('Schedule for user', str(update))
        id = update.message.chat_id
        text = update.message.text
        self._users.change_schedule(id, text)

    async def _raw_code(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        chat_id = update.message.chat_id
        emess = 'Success! Code complete!'

        user = self._users
        try:
            user.change_auth_code(chat_id, text)
            user.start_tg_client(chat_id)
            default_sch = '30 18 * * 5'
            user.change_schedule(chat_id, default_sch)
        except ValueError:
            emess = 'Bad value of command'
        except KeyError:
            emess = 'User not found, need first step /auth after send code'

        await update.message.reply_text(emess)

    async def _disable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = 'Your account is disable'
        try:
            self._users.disable(chat_id)
        except Exception as e:
            emess = 'Oops somthing broke - ' + str(e)

        await update.message.reply_text(emess)

    async def _enable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = 'Your account is enable'
        try:
            self._users.enable(chat_id)
        except Exception as e:
            emess = 'Oops somthing broke - ' + str(e)

        await update.message.reply_text(emess)

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
