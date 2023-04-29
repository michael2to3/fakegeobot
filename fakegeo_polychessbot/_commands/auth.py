from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from _type import Session, User


class Auth(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id

        if chat_id in self.bot._users:
            emess = "You already auth, if you want reauth you can /delete self"
            await update.message.reply_text(emess)
            return

        username = "Not change"
        if update.message.from_user is not None:
            username = update.message.from_user.full_name
        session_name = str(chat_id)

        text = update.message.text
        if update.message.text is None:
            await update.message.reply_text("Please enter your phone number")
            return

        emess = """
Send me auth code each char separated by a dot
For example: Login code: 61516
You put: /code 6.1.5.1.6
It's need to bypass protect telegram

*⚠️ Warning*: By creating an authentication session, you are granting this bot full access to your Telegram account. This includes the ability to read your messages, send messages on your behalf, and manage your account. Please ensure you trust the bot and its developers before proceeding. If you have any concerns, please review the bot's source code or contact the developers directly.
"""

        schedule = "30 18 * * 6"
        info = Session(session_name, username, chat_id, "", -1, schedule, "")
        user = User(self._api, info, True)

        try:
            phone_code_hash = await RequestCode.get(user, self._api)
            user.session.phone_code_hash = phone_code_hash
        except RuntimeError:
            emess = "Oops bad try access your account"
        except ValueError:
            emess = "Not correct message"
        except FloodWaitError as e:
            emess = f"Oops flood exception! Wait: {e.seconds} seconds"
        except OperationalError as e:
            self.logger.error(str(e))
            emess = "Oops database is fire!"
        else:
            self._db.save_user(user)
        finally:
            await update.message.reply_text(emess)
