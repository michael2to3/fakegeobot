import logging
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import FloodWaitError
from sqlite3 import OperationalError
from _commands import Command
from model import Session, User, Geolocation
from _user import RequestCode


class Auth(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id in self.bot.users:
            emess = "You already auth, if you want reauth you can /delete self"
            await update.message.reply_text(emess)
            return

        username = "Not change"
        if update.message.from_user is not None:
            username = update.message.from_user.full_name

        phone = update.message.text.split(" ")[1]
        if phone is None:
            await update.message.reply_text("Please enter your phone number")
            return

        emess = """
Send me auth code each char separated by a dot
For example: Login code: 61516
You put: /code 6.1.5.1.6
It's need to bypass protect telegram

<b>⚠️ Warning</b>: By creating an authentication session, you are granting this bot full access to your Telegram account. This includes the ability to read your messages, send messages on your behalf, and manage your account. Please ensure you trust the bot and its developers before proceeding. If you have any concerns, please review the bot's source code or contact the developers directly.
"""

        # @TODO remove default value
        geo = Geolocation(0, 0, 1)
        info = Session(
            session_name=str(chat_id),
            username=username,
            chat_id=chat_id,
            phone=phone,
            auth_code=None,
            phone_code_hash=None,
        )
        user = User(cron=None, location=geo, session=info, recipient="@me")

        try:
            user.session.phone_code_hash = await RequestCode.get(user, self.bot.api)
        except RuntimeError:
            emess = "Oops bad try access your account"
        except ValueError as e:
            emess = str(e)
        except FloodWaitError as e:
            emess = f"Oops flood exception! Wait: {e.seconds} seconds"
        except OperationalError as e:
            self.logger.error(str(e))
            emess = "Oops database is fire!"
        else:
            self.bot.db.save_user(user)
        finally:
            await update.message.reply_text(emess)
