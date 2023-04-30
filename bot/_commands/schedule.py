from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from croniter.croniter import CroniterBadCronError, CroniterNotAlphaError
from _cron import Cron
from _action import Fakelocation


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
        try:
            if user.cron is None:
                user.cron = Cron(
                    callback=Fakelocation(
                        self.bot.api, user.session, user.location, user.recipient
                    ).execute,
                    expression=schedule,
                    timeout=-1,
                )
                await user.cron.start()

            elif user.cron is not None and user.cron.expression != schedule:
                await user.cron.stop()
                user.cron = Cron(
                    callback=Fakelocation(
                        self.bot.api, user.session, user.location, user.recipient
                    ).execute,
                    expression=schedule,
                    timeout=-1,
                )
                await user.cron.start()
        except CroniterNotAlphaError as e:
            self.logger.error(str(e))
            emess = "Error, schedule not change"
        except CroniterBadCronError as e:
            self.logger.error(str(e))
            emess = "Not valid range"
        except ValueError as e:
            self.logger.error(str(e))
            emess = str(e)
        except Exception as e:
            emess = "Oops unknown error"
            self.logger.error(e)
        else:
            self.bot.db.save_user(self.bot.users[id])

        await update.message.reply_text(emess)
