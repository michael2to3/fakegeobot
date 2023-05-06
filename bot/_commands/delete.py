from .command import Command
from telegram import Update
from telegram.ext import ContextTypes
from ..text import TextHelper


class Delete(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text_helper = TextHelper(update, self.bot.users)
        chat_id = update.message.chat_id
        try:
            self.bot.db.delete_user(chat_id)
            del self.bot.users[chat_id]
        except KeyError as e:
            self.logger.error(str(e))
            await update.message.reply_text(text_helper.usertext("user_not_found"))
            return
        await update.message.reply_text(text_helper.usertext("user_deleted"))
