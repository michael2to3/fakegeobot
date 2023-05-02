from .command import Command
from telegram import Update
from telegram.ext import ContextTypes
from ..text import usertext as t


class Info(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(t("user_not_found", update, self.bot.users))
            return

        user = self.bot.users[chat_id]
        await update.message.reply_text(f"User: {user}")
