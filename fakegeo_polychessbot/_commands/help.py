from telegram import Update
from telegram.ext import ContextTypes
from _commands import Command


class Help(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            """
    /start - Start the bot 🚀
    /help - Show this help message 📚
    /auth PHONE_NUMBER - Authenticate with your phone number 📱
        Example: /auth +79992132533
    /code CODE - Enter the received code 🔢
        Example: /code 2.8.2.0.4
    /schedule CRON - Set a message sending schedule with a cron expression ⏰
        Example: /schedule 30 18 * * 5
    /send - Send your fake geolocation now 🌐
        Example: /send
    /delete - Delete your token and all related data 🗑️
        Example: /delete
    Cron help website: https://cron.help/#30_18_*_*_5
    More info: https://github.com/michael2to3/fakegeo-polychessbot
    Support: https://t.me/+EGnT6v3APokxMGYy
    """
        )
