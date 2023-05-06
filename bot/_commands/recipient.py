from .command import Command
from .._config import Config
from ..model import Geolocation
from telegram import Update
from telegram.ext import ContextTypes
from ..text import TextHelper


class Recipient(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        text_helper = TextHelper(update, self.bot.users)
        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(text_helper.usertext("user_not_found"))
            return

        if update.message.text.count(" ") < 1:
            await update.message.reply_text(
                text_helper.usertext("show_recipient").format(
                    self.bot.users[chat_id].recipient
                ),
            )
            return
        username = update.message.text.split(" ")[1]
        if not username:
            await update.message.reply_text(
                text_helper.usertext("recipient_not_change_username")
            )
            return

        self.bot.users[chat_id].recipient = username
        self.bot.db.save_user(self.bot.users[chat_id])
        await update.message.reply_text(text_helper.usertext("success"))

    def _from_location(self, update: Update) -> Geolocation:
        lat = update.message.location.latitude
        long = update.message.location.longitude
        interval = 600
        return Geolocation(lat=lat, long=long, interval=interval)

    def _from_text(self, update: Update) -> Geolocation:
        location = update.message.text.split(" ")[1:]
        if len(location) < 2 or len(location) > 3:
            self.logger.error("Not enough arguments")
            raise ValueError("Not enough arguments")

        lat = float(location[0])
        long = float(location[1])
        interval = (
            int(location[2]) if len(location) == 3 else Config().location_interval
        )

        return Geolocation(lat=lat, long=long, interval=interval)
