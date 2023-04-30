import logging
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import FloodWaitError
from sqlite3 import OperationalError
from _commands import Command
from model import Session, User
from _user import RequestCode


class Reauth(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text("User not found")
            return

        await update.message.reply_text(
            "You already auth, your session will be *overwritten*\nUsing this command very often yuo can get *banned* by telegram",
            parse_mode="Markdown",
        )

        emess = """
Send me auth code each char separated by a dot
For example: Login code: 61516
You put: /code 6.1.5.1.6
It's need to bypass protect telegram

*⚠️ Warning*: By creating an authentication session, you are granting this bot *full access* to your Telegram account. This includes the ability to read your messages, send messages on your behalf, and manage your account. Please ensure you trust the bot and its developers before proceeding. If you have any concerns, please review the bot's source code or contact the developers directly.
"""

        user = self.bot.users[chat_id]
        if not user.session.phone:
            await update.message.reply_text(
                "Hmm, you don't have a phone number yet\nTry /delete your self and /auth again"
            )
            self.logger.warn(f"User doesn't have a phone number: {chat_id}")
            return
        try:
            user.session.phone_code_hash = await RequestCode.get(user, self.bot.api)
        except RuntimeError:
            emess = "Oops bad try access your account"
        except FloodWaitError as e:
            emess = f"Oops flood exception! Wait: {e.seconds} seconds"
        except OperationalError as e:
            self.logger.error(str(e))
            emess = "Oops database is fire!"
        else:
            self.bot.users[chat_id] = user
            self.bot.db.save_user(user)
        finally:
            await update.message.reply_text(emess, parse_mode="Markdown")
