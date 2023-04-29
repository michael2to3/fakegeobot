from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command


class Code(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        auth_code = update.message.text
        if auth_code is None:
            await update.message.reply_text("Bad value of command")
            return

        chat_id = update.message.chat_id
        emess = "Success! Code complete!"

        try:
            self.bot._users[chat_id].session.auth_code = int(auth_code)
        except ValueError:
            emess = "Bad value of command"
        except KeyError:
            emess = "User not found, need first step /auth after send code"

        await update.message.reply_text(emess)
