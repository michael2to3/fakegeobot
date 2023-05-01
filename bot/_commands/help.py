from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


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
/disable - Disable a command or feature 🔕
    Example: /disable send
/enable - Enable a command or feature 🔔
    Example: /enable send
/delete - Delete your token and all related data 🗑️
    Example: /delete
/location - Set or update your fake geolocation coordinates 📍
    Example: /location 37.7749 -122.4194
/recipient - Set or update the recipient for the fake geolocation 🎯
    Example: /recipient @username
/reauth - Reauthenticate with your phone number if needed 🔄
    Example: /reauth
/info - Get information about your current settings ℹ️
    Example: /info

Cron help website: https://cron.help/#30_18_*_*_5
More info: https://github.com/michael2to3/fakegeo-polychessbot
Support: https://t.me/+EGnT6v3APokxMGYy
    """
        )
