from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from _type import Session, User


class Delete(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        try:
            await self.bot._users.delete(chat_id)
        except KeyError as e:
            self.bot.logger.error(str(e))
            await update.message.reply_text("Your token is not registered")
            return
        await update.message.reply_text("Your account was deleted!")
