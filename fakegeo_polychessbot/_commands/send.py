from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from _type import Session, User


class Send(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        emess = "Well done"
        try:
            await self.bot._users.perform_checkin(chat_id)
        except cronaction.FloodError as e:
            emess = f"Flood detection! Wait {e.timeout}"
        except AuthKeyUnregisteredError as e:
            self.logger.error(str(e))
            emess = "Your token is not registered"
        except Exception as e:
            self.logger.error(str(e))
            emess = "Oops something went wrong"
        finally:
            await update.message.reply_text(emess)
