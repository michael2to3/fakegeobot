from sqlite3 import OperationalError

from .command import Command
from .._user import RequestCode
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import FloodWaitError


class Reauth(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(self.text_helper.usertext("user_not_found"))
            return

        await update.message.reply_text(
            self.text_helper.usertext("reauth_message"),
            parse_mode="Markdown",
        )

        emess = self.text_helper.usertext("auth_code_sent")

        user = self.bot.users[chat_id]
        if not user.session.phone:
            await update.message.reply_text(
                self.text_helper.usertext("user_not_change_phone")
            )
            self.logger.warn(f"User doesn't have a phone number: {chat_id}")
            return
        try:
            user.session.phone_code_hash = await RequestCode.get(user, self.bot.api)
        except RuntimeError:
            emess = self.text_helper.usertext("auth_code_not_sent")
        except FloodWaitError as e:
            emess = self.text_helper.usertext("flood_wait_error").format(str(e.seconds))
        else:
            self.bot.users[chat_id] = user
            self.bot.db.save_user(user)
        finally:
            await update.message.reply_text(emess, parse_mode="Markdown")
