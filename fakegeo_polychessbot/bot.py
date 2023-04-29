import logging
from sqlite3 import OperationalError
from croniter.croniter import CroniterBadCronError, CroniterNotAlphaError

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telethon.errors import AuthKeyUnregisteredError, FloodWaitError

from usermanager import UserManager
from session_name import SessionName
from type import Api, UserInfo
from user import User
import cronaction


class Bot:
    logger: logging.Logger
    _api: Api
    _app: Application
    _users: UserManager
    _path_db: str

    def __init__(self, api: Api, token: str, path_db: str, name_db: str):
        self.logger = logging.getLogger(__name__)
        self._app = Application.builder().token(token).build()
        self._api = api
        self._path_db = path_db
        self._users = UserManager(path_db, name_db)
        self._users.restore()

    async def _start(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            """
Hi there! 🤖\n
To enable this feature, follow these steps:
1) Authenticate by typing: /auth {YOUR_PHONE_NUMBER}
   Example: /auth +79992132533
2) Enter the code you receive as: /code {CODE}
   Example: If the code is 28204, enter: /code 2.8.2.0.4
3) To change the message sending schedule, type: /schedule {CRON_EXPRESSION}
   Example: /schedule 30 18 * * 5
   Need help with cron expressions? Visit: https://cron.help/
For more information, check the GitHub repository:
    https://github.com/michael2to3/fakegeo-polychessbot
"""
        )

    async def _help(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        message = """
/start - Start the bot 🚀
/help - Show this help message 📚
/auth PHONE_NUMBER - Authenticate with your phone number 📱
    Example: /auth +79992132533
/code CODE - Enter the received code 🔢
    Example: /code 2.8.2.0.4
/schedule CRON - Set a message sending schedule with a cron expression ⏰
    Example: /schedule 30 18 * * 5
/send - Send your fake geolocation now 🌐
    Example: /send
/delete - Delete your token and all related data 🗑️
    Example: /delete
Cron help website: https://cron.help/#30_18_*_*_5
More info: https://github.com/michael2to3/fakegeo-polychessbot
Support: https://t.me/+EGnT6v3APokxMGYy
"""
        await update.message.reply_text(message)

    async def _auth(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if self._users.check_exist(chat_id):
            emess = "You already auth, if you want reauth you can /delete self"
            await update.message.reply_text(emess)
            return

        username = "Not change"
        if update.message.from_user is not None:
            username = update.message.from_user.full_name
        sid = str(chat_id)
        session_name = self._path_db + SessionName().get_session_name_base(sid)

        text = update.message.text
        if update.message.text is None:
            await update.message.reply_text("Please enter your phone number")
            return

        emess = """
Send me auth code each char separated by a dot
For example: Login code: 61516
You put: /code 6.1.5.1.6
It's need to bypass protect telegram
"""

        schedule = "30 18 * * 6"
        info = UserInfo(session_name, username, chat_id, "", -1, schedule, "")
        user = User(self._api, info, True)

        try:
            self._users.update_user(user)
            self._users.update_phone(chat_id, text)
            phone_code_hash = await self._users.request_code(chat_id)
            self._users.update_phone_code_hash(chat_id, phone_code_hash)

        except RuntimeError:
            emess = "Oops bad try access your account"
        except ValueError:
            emess = "Not correct message"
        except FloodWaitError as e:
            emess = f"Oops flood exception! Wait: {e.seconds} seconds"
        except OperationalError as e:
            self.logger.error(str(e))
            emess = "Oops database is fire!"
        else:
            self._users.save(chat_id)
        finally:
            await update.message.reply_text(emess)

    async def _send_now(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Well done"
        try:
            await self._users.perform_checkin(chat_id)
        except cronaction.FloodError as e:
            emess = f"Flood detection! Wait {e.timeout}"
        except AuthKeyUnregisteredError as e:
            self.logger.error(str(e))
            emess = "Your token is not registered"
        except Exception as e:
            self.logger.error(str(e))
            emess = "Oops something went wrong"
        finally:
            await update.message.reply_text(emess)

    async def _delete(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        try:
            await self._users.delete(chat_id)
        except KeyError as e:
            self.logger.error(str(e))
            await update.message.reply_text("Your token is not registered")
            return
        await update.message.reply_text("Your account was deleted!")

    async def _schedule(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        id = update.message.chat_id
        text = update.message.text

        if text is None:
            await update.message.reply_text("Please enter your schedule")
            return

        if text.find(" ") == -1:
            sch = f"Your schedule {self._users.get_user(id)._info._schedule}"
            await update.message.reply_text(sch)
            return

        emess = "Done!"
        try:
            self._users.update_schedule(id, text)
        except CroniterNotAlphaError as e:
            self.logger.error(str(e))
            emess = "Error, schedule not change"
        except CroniterBadCronError as e:
            self.logger.error(str(e))
            emess = "Not valid range"
        except ValueError as e:
            self.logger.error(str(e))
            emess = str(e)
        except Exception as e:
            emess = "Oops unknown error"
            self.logger.error(e)
        else:
            self._users.save(id)

        await update.message.reply_text(emess)

    async def _raw_code(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text is None:
            text = "Not change"

        chat_id = update.message.chat_id
        emess = "Success! Code complete!"

        users = self._users
        try:
            users.update_auth_code(chat_id, text)
            default_sch = "30 18 * * 6"
            users.update_schedule(chat_id, default_sch)
        except ValueError:
            emess = "Bad value of command"
        except KeyError:
            emess = "User not found, need first step /auth after send code"

        await update.message.reply_text(emess)

    async def _disable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Your account is disable"
        try:
            self._users.disable(chat_id)
        except Exception as e:
            emess = "Oops somthing broke - " + str(e)

        await update.message.reply_text(emess)

    async def _enable(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Your account is enable"
        try:
            self._users.enable(chat_id)
        except Exception as e:
            emess = "Oops somthing broke - " + str(e)

        await update.message.reply_text(emess)

    async def _handle_command(
        self, command: str, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if update.message is None:
            self.logger.error(f"Message is None in command: {command}")
            return

        command = update.message.text.split(" ")[0].lstrip("/")

        handlers = {
            "start": self._start,
            "help": self._help,
            "auth": self._auth,
            "code": self._raw_code,
            "schedule": self._schedule,
            "send": self._send_now,
            "disable": self._disable,
            "enable": self._enable,
            "delete": self._delete,
        }

        handler = handlers.get(command)
        if handler:
            try:
                await handler(update, context)
            except Exception as e:
                self.logger.error(f"Error while handling the command: {command}, {e}")
                await update.message.reply_text(
                    f"Oops! An error occurred while handling the command: {command}."
                )
        else:
            self.logger.warn(f"Unknown command: {command}")
            await update.message.reply_text(f"Unknown command: {command}")

    def run(self) -> None:
        app = self._app
        commands = [
            "start",
            "help",
            "auth",
            "code",
            "schedule",
            "send",
            "disable",
            "enable",
            "delete",
        ]

        for command in commands:
            app.add_handler(
                CommandHandler(
                    command, lambda u, c: self._handle_command(command, u, c)
                )
            )
        app.run_polling()
