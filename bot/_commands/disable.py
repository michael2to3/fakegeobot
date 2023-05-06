from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


class Disable(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in self._context.users:
            await update.message.reply_text(self.text_helper.usertext("user_not_found"))
            self.logger.info(f"User {chat_id} not found")
            return

        user = self._context.users[chat_id]
        if user.cron is None:
            await update.message.reply_text(
                self.text_helper.usertext("cron_not_initialized")
            )
            self.logger.info(f"User {chat_id} not initialized cron")
            return

        user.cron.stop()

        await update.message.reply_text(self.text_helper.usertext("cron_disabled"))
