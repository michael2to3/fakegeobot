from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command
from model import Geolocation


class Recipient(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text("User not found")
            return

        if update.message.text.count(" ") < 1:
            await update.message.reply_text(
                f"Your recipient: {self.bot.users[chat_id].recipient}"
            )
            return
        username = update.message.text.split(" ")[1]
        if not username:
            await update.message.reply_text("Please enter username")
            return

        self.bot.users[chat_id].recipient = username
        self.bot.db.save_user(self.bot.users[chat_id])
        await update.message.reply_text("Success!")

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

        interval = 600
        lat = float(location[0])
        long = float(location[1])
        interval = int(location[2]) if len(location) == 3 else 10

        return Geolocation(lat=lat, long=long, interval=interval)
