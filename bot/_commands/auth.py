from .command import Command
from .._user import RequestCode
from ..model import Session, User
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import FloodWaitError
from .._config import Config
from ..text import TextHelper


class Auth(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self._config = Config()

    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        text_helper = TextHelper(update, self.bot.users)

        if chat_id in self.bot.users:
            await update.message.reply_text(
                text_helper.usertext("user_already_registered"),
                parse_mode="Markdown",
            )
            return

        username = "Not change"
        if update.message.from_user is not None:
            username = update.message.from_user.full_name

        if update.message.text.count(" ") < 1:
            await update.message.reply_text(
                text_helper.usertext("enter_auth_code"), parse_mode="Markdown"
            )
            return
        phone = update.message.text.split(" ")[1]
        if phone is None:
            await update.message.reply_text(
                text_helper.usertext("enter_phone"), parse_mode="Markdown"
            )
            return

        emess = text_helper.usertext("auth_code_sent")

        info = Session(
            session_name=str(chat_id),
            username=username,
            chat_id=chat_id,
            phone=phone,
            auth_code=None,
            phone_code_hash=None,
        )
        location = None if self._config.location is None else self._config.location
        recipient = None if self._config.recipient is None else self._config.recipient
        language_code = update.message.from_user.language_code
        language = language_code.split("_")[0]
        user = User(
            cron=None,
            location=location,
            session=info,
            recipient=recipient,
            language=language,
        )

        try:
            user.session.phone_code_hash = await RequestCode.get(user, self.bot.api)
        except RuntimeError as e:
            self.logger.error(e)
            emess = text_helper.usertext("auth_code_not_sent")
        except FloodWaitError as e:
            self.logger.error(e)
            emess = text_helper.usertext("flood_wait_error")
        else:
            self.bot.users[chat_id] = user
            self.bot.db.save_user(user)
        finally:
            await update.message.reply_text(emess, parse_mode="Markdown")
