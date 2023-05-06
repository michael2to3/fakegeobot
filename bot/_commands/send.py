from .._action import Fakelocation
from .._commands import Command
from telegram import Update
from telegram.ext import ContextTypes
from telethon.errors import AuthKeyUnregisteredError
from ..text import TextHelper


class Send(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        text_helper = TextHelper(update, self.bot.users)
        emess = "Well done"
        try:
            user = self.bot.users[chat_id]

            if user.location is None:
                await update.message.reply_text(text_helper.usertext("need_location"))
                return
            if user.recipient is None:
                await update.message.reply_text(text_helper.usertext("need_recipient"))
                return

            action = Fakelocation(
                self.bot.api, user.session, user.location, user.recipient
            )
            await action.execute()
        except AuthKeyUnregisteredError as e:
            self.logger.error(str(e))
            emess = "Your token is not registered"
        except ConnectionError as e:
            self.logger.error(str(e))
            emess = "Connection error"
        finally:
            await update.message.reply_text(emess)
