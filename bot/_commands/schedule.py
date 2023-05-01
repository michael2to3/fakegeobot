from .._action import Fakelocation
from .._commands import Command
from .._cron import Cron
from .._config import Config
from croniter.croniter import CroniterBadCronError, CroniterNotAlphaError
from telegram import Update
from telegram.ext import ContextTypes


class Schedule(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        id = update.message.chat_id
        schedule = update.message.text
        user = self.bot.users[id]

        if schedule.find(" ") == -1:
            await update.message.reply_text(
                f"Your schedule {user.cron.expression if user.cron is not None else None}"
            )
            return

        schedule = " ".join(schedule.split(" ")[1:])

        if user.location is None:
            await update.message.reply_text("Need change location")
            return

        if user.recipient is None:
            await update.message.reply_text("Need change recipient")
            return

        emess = "Done!"
        if user.cron is not None:
            user.cron.stop()

        try:
            user.cron = Cron(
                callback=Fakelocation(
                    self.bot.api, user.session, user.location, user.recipient
                ).execute,
                cron_expression=schedule,
                callback_timeout=user.cron.timeout
                if user.cron is not None
                else Config().cron_timeout,
            )

            user.cron.start()
        except CroniterNotAlphaError as e:
            self.logger.error(str(e))
            emess = "Error, schedule not change"
        except CroniterBadCronError as e:
            self.logger.error(str(e))
            emess = "Not valid range"
        else:
            self.bot.db.save_user(self.bot.users[id])

        await update.message.reply_text(emess)
