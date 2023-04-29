from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from _type import Session, User


class Enable(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Your account is enable"
        try:
            self.bot._users.enable(chat_id)
        except Exception as e:
            emess = "Oops somthing broke - " + str(e)

        await update.message.reply_text(emess)
