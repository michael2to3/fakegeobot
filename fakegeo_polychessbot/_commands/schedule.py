from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from _type import Session, User


class Schedule(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        id = update.message.chat_id
        text = update.message.text

        if text is None:
            await update.message.reply_text("Please enter your schedule")
            return

        if text.find(" ") == -1:
            sch = f"Your schedule {self.bot._users.get_user(id)._info._schedule}"
            await update.message.reply_text(sch)
            return

        emess = "Done!"
        try:
            self.bot._users.update_schedule(id, text)
        except CroniterNotAlphaError as e:
            self.bot.logger.error(str(e))
            emess = "Error, schedule not change"
        except CroniterBadCronError as e:
            self.bot.logger.error(str(e))
            emess = "Not valid range"
        except ValueError as e:
            self.bot.logger.error(str(e))
            emess = str(e)
        except Exception as e:
            emess = "Oops unknown error"
            self.bot.logger.error(e)
        else:
            self.bot._users.save(id)

        await update.message.reply_text(emess)
