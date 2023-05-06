from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


class Info(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id not in self._context.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(self.text_helper.usertext("user_not_found"))
            return

        user = self._context.users[chat_id]
        await update.message.reply_text(f"User: {user}")
