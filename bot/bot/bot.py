import logging
import traceback
from sqlite3 import OperationalError
from typing import Dict
from ..text import TextHelper
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from .botcontext import BotContext
from .._config import Config

from .._commands import (
    Auth,
    Code,
    Delete,
    Disable,
    Enable,
    Help,
    Info,
    Location,
    Reauth,
    Recipient,
    Schedule,
    Send,
    Start,
    Language,
)
from .._db import DatabaseHandler
from .abstract_bot import AbstractBot
from ..model import ApiApp, User


class Bot(AbstractBot):
    logger: logging.Logger
    _api: ApiApp
    _app: Application
    _users: Dict[int, User]
    _db: DatabaseHandler

    def __init__(self, api: ApiApp, token: str, db: DatabaseHandler, config: Config):
        self.logger = logging.getLogger(__name__)
        self._app = Application.builder().token(token).build()
        self._api = api
        self._db = db
        users = list(db.load_all_users())
        self._users = {user.session.chat_id: user for user in users}
        self._context = BotContext(api, self._users, self._db, config)

    async def _handle_command(
        self, command: str, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if update.message is None:
            self.logger.error(f"Message is None in command: {command}")
            return

        command = update.message.text.split(" ")[0].lstrip("/")

        text_helper = TextHelper(update, self.users)
        handlers = {
            "start": Start(self._context, text_helper),
            "help": Help(self._context, text_helper),
            "auth": Auth(self._context, text_helper),
            "code": Code(self._context, text_helper),
            "schedule": Schedule(self._context, text_helper),
            "send": Send(self._context, text_helper),
            "disable": Disable(self._context, text_helper),
            "enable": Enable(self._context, text_helper),
            "delete": Delete(self._context, text_helper),
            "location": Location(self._context, text_helper),
            "recipient": Recipient(self._context, text_helper),
            "reauth": Reauth(self._context, text_helper),
            "info": Info(self._context, text_helper),
            "language": Language(self._context, text_helper),
        }

        handler = handlers.get(command)
        if handler:
            try:
                await handler.handle(update, context)
            except ConnectionError as e:
                self.logger.error(f"ConnectionError: {e}")

                await update.message.reply_text(
                    text_helper.usertext("connection_error")
                )
            except ValueError as e:
                self.logger.error(f"ValueError: {e}")
                await update.message.reply_text(text_helper.usertext("value_error"))
            except OperationalError as e:
                error_traceback = traceback.format_exc()
                self.logger.error(
                    f"Error while handling the command: {command}, {e}\n{error_traceback}"
                )
                await update.message.reply_text(text_helper.usertext("database_error"))
            except Exception as e:
                error_traceback = traceback.format_exc()
                self.logger.error(
                    f"Error while handling the command: {command}, {e}\n{error_traceback}"
                )
                await update.message.reply_text(text_helper.usertext("unknown_error"))
        else:
            self.logger.warning(f"Unknown command: {command}")
            await update.message.reply_text(
                text_helper.usertext("unknown_command").format(command)
            )

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
            "location",
            "recipient",
            "reauth",
            "info",
            "language",
        ]

        for command in commands:
            app.add_handler(
                CommandHandler(
                    command, lambda u, c: self._handle_command(command, u, c)
                )
            )

        for user in self._users.values():
            if user.cron:
                user.cron.start()

        app.run_polling()

    @property
    def users(self) -> Dict[int, User]:
        return self._users

    @property
    def db(self) -> DatabaseHandler:
        return self._db

    @property
    def api(self) -> ApiApp:
        return self._api
