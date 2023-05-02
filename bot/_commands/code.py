from .command import Command
from ..model import User
from .._config import Config
from .._cron import Cron
from .._action import Fakelocation
from .._normalizer import AuthCode
from telegram import Update
from telegram.ext import ContextTypes
from gettext import gettext as t


class Code(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self._config = Config()

    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        auth_code = update.message.text.split(" ")[1]
        chat_id = update.message.chat_id

        if auth_code is None:
            await update.message.reply_text(t("enter_auth_code"), parse_mode="Markdown")
            return
        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(t("user_not_found"), parse_mode="Markdown")
            return

        user = self.bot.users[chat_id]
        code = AuthCode.normalize(auth_code)
        user.session.auth_code = int(code)
        user.cron = self._get_cron(user)
        user.cron.start()
        self.bot.db.save_user(user)
        self.bot.users[chat_id] = user
        await update.message.reply_text(t("success"), parse_mode="Markdown")

    def _get_cron(self, user: User):
        location = self._config.location
        recipient = self._config.recipient
        expression = self._config.cron_expression
        timeout = self._config.cron_timeout
        if user.cron is None:
            return self._default_cron(user)
        else:
            user.cron.stop()

        if user.location is not None:
            location = user.location

        if user.recipient is not None:
            recipient = user.recipient

        if user.cron.expression is not None:
            expression = user.cron.expression

        if user.cron.timeout is not None:
            timeout = user.cron.timeout

        return Cron(
            callback=Fakelocation(
                self.bot.api, user.session, location, recipient
            ).execute,
            cron_expression=expression,
            callback_timeout=timeout,
        )

    def _default_cron(self, user: User):
        return Cron(
            callback=Fakelocation(
                self.bot.api,
                user.session,
                self._config.location,
                self._config.recipient,
            ).execute,
            cron_expression=self._config.cron_expression,
            callback_timeout=self._config.cron_timeout,
        )
