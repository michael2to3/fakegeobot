from .command import Command
from ..model import Geolocation
from telegram import Update
from telegram.ext import ContextTypes


class Location(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in self.context.users:
            self.logger.warning(f"User not found: {chat_id}")
            await update.message.reply_text(self.text_helper.usertext("user_not_found"))
            return

        location = None
        if update.message.location:
            location = self._from_location(update)
        else:
            if update.message.text.count(" ") <= 1:
                await update.message.reply_text(
                    self.text_helper.usertext("location_show").format(
                        self.context.users[chat_id].location
                    )
                )
                return
            location = self._from_text(update)

        self.context.users[chat_id].location = location
        self.context.db.save_user(self.context.users[chat_id])
        await update.message.reply_text(self.text_helper.usertext("success"))

    def _from_location(self, update: Update) -> Geolocation:
        lat = update.message.location.latitude
        long = update.message.location.longitude
        interval = self.context.config.location.interval
        return Geolocation(lat=lat, long=long, interval=interval)

    def _from_text(self, update: Update) -> Geolocation:
        location = update.message.text.split(" ")[1:]
        if len(location) < 2 or len(location) > 4:
            self.logger.error("Not enough arguments")
            raise ValueError("Not enough arguments")

        interval = 600
        lat = float(location[0])
        long = float(location[1])
        interval = (
            int(location[2])
            if len(location) == 3
            else self.context.config.location.interval
        )

        return Geolocation(lat=lat, long=long, interval=interval)
