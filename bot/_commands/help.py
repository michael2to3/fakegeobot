from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


class Help(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.text_helper.usertext("help"))
