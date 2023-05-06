from .command import Command
from ..model import User
from .._cron import Cron
from .._action import Fakelocation
from .._normalizer import AuthCode
from telegram import Update
from telegram.ext import ContextTypes


class Code(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        auth_code = update.message.text.split(" ")[1]
        chat_id = update.message.chat_id

        if auth_code is None:
            await update.message.reply_text(
                self.text_helper.usertext("enter_auth_code"), parse_mode="Markdown"
            )
            return
        if chat_id not in self._context.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(
                self.text_helper.usertext("user_not_found"), parse_mode="Markdown"
            )
            return

        user = self._context.users[chat_id]
        code = AuthCode.normalize(auth_code)
        user.session.auth_code = int(code)
        user.cron = self._get_cron(user)
        user.cron.start()
        self._context.db.save_user(user)
        self._context.users[chat_id] = user
        await update.message.reply_text(
            self.text_helper.usertext("success"), parse_mode="Markdown"
        )

    def _get_cron(self, user: User):
        config = self._context.config
        return Cron.create_cron(
            config,
            callback=Fakelocation.create_fakelocation(
                config, self._context.api, user.session, user.location, user.recipient
            ).execute,
            cron_expression=user.cron.expression if user.cron is not None else None,
            callback_timeout=user.cron.timeout
            if user.cron is not None
            else config.cron_timeout,
        )
