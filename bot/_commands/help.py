from .command import Command
from telegram import Update
from telegram.ext import ContextTypes
from ..text import TextHelper


class Help(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text_helper = TextHelper(update, self.bot.users)
        await update.message.reply_text(text_helper.usertext("help"))
