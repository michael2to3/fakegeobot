from .command import Command
from ..model import Geolocation
from telegram import Update
from telegram.ext import ContextTypes
from ..text import usertext as t


class Location(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(t("user_not_found"))
            return

        location = None
        if update.message.location:
            location = self._from_location(update)
        else:
            if update.message.text.count(" ") <= 1:
                await update.message.reply_text(
                    t("location_show").format(self.bot.users[chat_id].location)
                )
                return
            location = self._from_text(update)

        self.bot.users[chat_id].location = location
        self.bot.db.save_user(self.bot.users[chat_id])
        await update.message.reply_text("Success!")

    def _from_location(self, update: Update) -> Geolocation:
        lat = update.message.location.latitude
        long = update.message.location.longitude
        interval = 600
        return Geolocation(lat=lat, long=long, interval=interval)

    def _from_text(self, update: Update) -> Geolocation:
        location = update.message.text.split(" ")[1:]
        if len(location) < 2 or len(location) > 4:
            self.logger.error("Not enough arguments")
            raise ValueError("Not enough arguments")

        interval = 600
        lat = float(location[0])
        long = float(location[1])
        interval = int(location[2]) if len(location) == 3 else 60

        return Geolocation(lat=lat, long=long, interval=interval)
