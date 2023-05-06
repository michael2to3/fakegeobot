from .._action import Fakelocation
from .._commands import Command
from .._cron import Cron
from croniter.croniter import CroniterBadCronError, CroniterNotAlphaError
from telegram import Update
from telegram.ext import ContextTypes


class Schedule(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        schedule = update.message.text
        user = self.bot.users[chat_id]

        if schedule.find(" ") == -1:
            await update.message.reply_text(
                self.text_helper.usertext("cron_show_expression").format(
                    user.cron.expression if user.cron is not None else "None"
                )
            )
            return

        schedule = " ".join(schedule.split(" ")[1:])

        if user.location is None:
            await update.message.reply_text(self.text_helper.usertext("need_location"))
            return

        if user.recipient is None:
            await update.message.reply_text(self.text_helper.usertext("need_recipient"))
            return

        emess = self.text_helper.usertext("cron_set_schedule")
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
                else self._config.cron_timeout,
            )

            user.cron.start()
        except CroniterNotAlphaError | CroniterBadCronError as e:
            self.logger.error(str(e))
            emess = self.text_helper.usertext("cron_invalid_expression")
        else:
            self.bot.db.save_user(self.bot.users[chat_id])

        await update.message.reply_text(emess)
