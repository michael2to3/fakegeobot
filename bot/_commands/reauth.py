from sqlite3 import OperationalError

from .command import Command
from .._user import RequestCode
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import FloodWaitError
from ..text import usertext as t


class Reauth(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(t("user_not_found", update, self.bot.users))
            return

        await update.message.reply_text(
            t("reauth_message", update, self.bot.users),
            parse_mode="Markdown",
        )

        emess = t("auth_code_sent", update, self.bot.users)

        user = self.bot.users[chat_id]
        if not user.session.phone:
            await update.message.reply_text(
                t("user_not_change_phone", update, self.bot.users),
            )
            self.logger.warn(f"User doesn't have a phone number: {chat_id}")
            return
        try:
            user.session.phone_code_hash = await RequestCode.get(user, self.bot.api)
        except RuntimeError:
            emess = t("auth_code_not_sent", update, self.bot.users)
        except FloodWaitError as e:
            emess = t("flood_wait_error", update, self.bot.users).format(str(e.seconds))
        except OperationalError as e:
            self.logger.error(str(e))
            emess = t("db_error", update, self.bot.users)
        else:
            self.bot.users[chat_id] = user
            self.bot.db.save_user(user)
        finally:
            await update.message.reply_text(emess, parse_mode="Markdown")
