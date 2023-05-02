import logging
import traceback
from sqlite3 import OperationalError
from typing import Dict
from gettext import gettext as t
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from ._commands import (
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
)
from ._db import DatabaseHandler
from .abstract_bot import AbstractBot
from .model import ApiApp, User


class Bot(AbstractBot):
    logger: logging.Logger
    _api: ApiApp
    _app: Application
    _users: Dict[int, User]
    _db: DatabaseHandler

    def __init__(self, api: ApiApp, token: str, db: DatabaseHandler):
        self.logger = logging.getLogger(__name__)
        self._app = Application.builder().token(token).build()
        self._api = api
        self._db = db
        users = list(db.load_all_users())
        self._users = {user.session.chat_id: user for user in users}

    async def _handle_command(
        self, command: str, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        if update.message is None:
            self.logger.error(f"Message is None in command: {command}")
            return

        command = update.message.text.split(" ")[0].lstrip("/")

        handlers = {
            "start": Start(self),
            "help": Help(self),
            "auth": Auth(self),
            "code": Code(self),
            "schedule": Schedule(self),
            "send": Send(self),
            "disable": Disable(self),
            "enable": Enable(self),
            "delete": Delete(self),
            "location": Location(self),
            "recipient": Recipient(self),
            "reauth": Reauth(self),
            "info": Info(self),
        }

        handler = handlers.get(command)
        if handler:
            try:
                await handler.handle(update, context)
            except ConnectionError as e:
                self.logger.error(f"ConnectionError: {e}")
                await update.message.reply_text(t("connection_error"))
            except ValueError as e:
                self.logger.error(t("value_error"))
                await update.message.reply_text(f"ValueError: {e}")
            except OperationalError as e:
                error_traceback = traceback.format_exc()
                self.logger.error(
                    f"Error while handling the command: {command}, {e}\n{error_traceback}"
                )
                await update.message.reply_text(t("database_error"))
            except Exception as e:
                error_traceback = traceback.format_exc()
                self.logger.error(
                    f"Error while handling the command: {command}, {e}\n{error_traceback}"
                )
                await update.message.reply_text(t("unknown_error"))
        else:
            self.logger.warn(f"Unknown command: {command}")
            await update.message.reply_text(t("unknown_command").format(command))

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
