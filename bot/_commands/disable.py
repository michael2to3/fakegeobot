from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command


class Disable(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Your account is disable"
        try:
            self.bot.users[chat_id].cron.stop()
        except Exception as e:
            self.logger.error(str(e))
            emess = f"Oops somthing broke - {str(e)}"

        await update.message.reply_text(emess)
