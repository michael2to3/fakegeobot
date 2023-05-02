from .command import Command
from telegram import Update
from telegram.ext import ContextTypes
from ..text import usertext as t


class Start(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(t("start", update, self.bot.users))
