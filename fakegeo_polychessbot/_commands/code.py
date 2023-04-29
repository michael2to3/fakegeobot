from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command


class Code(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text is None:
            text = "Not change"

        chat_id = update.message.chat_id
        emess = "Success! Code complete!"

        users = self.bot._users
        try:
            users.update_auth_code(chat_id, text)
            default_sch = "30 18 * * 6"
            users.update_schedule(chat_id, default_sch)
        except ValueError:
            emess = "Bad value of command"
        except KeyError:
            emess = "User not found, need first step /auth after send code"

        await update.message.reply_text(emess)
