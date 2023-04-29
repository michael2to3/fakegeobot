from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from croniter.croniter import CroniterBadCronError, CroniterNotAlphaError


class Schedule(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        id = update.message.chat_id
        schedule = update.message.text

        if schedule is None:
            await update.message.reply_text("Please enter your schedule")
            return

        if schedule.find(" ") == -1:
            await update.message.reply_text(f"Your schedule {self.bot._users[id].session.schedule}")
            return

        emess = "Done!"
        try:
            self.bot._users[id].cron.cron_expression = schedule
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
            self.bot._db.save_user(self.bot._users[id])

        await update.message.reply_text(emess)
