from .command import Command
from telegram import Update
from telegram.ext import ContextTypes


class Start(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            """
Hi there! 🤖\n
To enable this feature, follow these steps:
1) Authenticate by typing: /auth {YOUR_PHONE_NUMBER}
   Example: /auth +79992132533
2) Enter the code you receive as: /code {CODE}
   Example: If the code is 28204, enter: /code 2.8.2.0.4
3) To change the message sending schedule, type: /schedule {CRON_EXPRESSION}
   Example: /schedule 30 18 * * 5
4) You can try send message now by typing: /send
To show this help message, type: /help
Need help with cron expressions? Visit: https://cron.help/
For more information, check the GitHub repository:
   https://github.com/michael2to3/fakegeo-polychessbot
   """
        )
