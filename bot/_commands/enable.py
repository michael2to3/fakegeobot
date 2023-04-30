from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


class Enable(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in self.bot.users:
            await update.message.reply_text("User not found")
            self.logger.info(f"User {chat_id} not found")
            return

        user = self.bot.users[chat_id]
        if user.cron is None:
            await update.message.reply_text("Your account not initialized cron")
            self.logger.info(f"User {chat_id} not initialized cron")
            return

        self.bot.users[chat_id].cron.start()

        await update.message.reply_text("Your account is enable")
