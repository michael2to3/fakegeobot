from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import AuthKeyUnregisteredError
from _commands import Command
from _action import Fakelocation


class Send(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Well done"
        try:
            action = Fakelocation(self.bot.api, self.bot.users[chat_id])
            await action.execute()
        except AuthKeyUnregisteredError as e:
            self.logger.error(str(e))
            emess = "Your token is not registered"
        finally:
            await update.message.reply_text(emess)
