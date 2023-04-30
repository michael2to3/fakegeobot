from .command import Command
from .._normalizer import AuthCode
from telegram import Update
from telegram.ext import ContextTypes


class Code(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        auth_code = update.message.text.split(" ")[1]
        chat_id = update.message.chat_id

        if auth_code is None:
            await update.message.reply_text("Please enter auth code")
            return
        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text("User not found")
            return

        emess = "Success! Code complete!"

        try:
            code = AuthCode.normalize(auth_code)
            self.bot.users[chat_id].session.auth_code = int(code)
            self.bot.db.save_user(self.bot.users[chat_id])
        except ValueError as e:
            emess = "ValueError: " + str(e)

        await update.message.reply_text(emess)
