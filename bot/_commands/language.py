from .command import Command
from telegram import Update
from telegram.ext import ContextTypes
from ..text import TextHelper


class Language(Command):
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        text_helper = TextHelper(update, self.bot.users)

        if chat_id not in self.bot.users:
            self.logger.warn(f"User not found: {chat_id}")
            await update.message.reply_text(text_helper.usertext("user_not_found"))
            return

        user = self.bot.users[chat_id]
        avaliable_languages = [
            "en",
            "ru",
        ]

        lang = update.message.text.lower().strip().split(" ")
        if len(lang) != 2:
            await update.message.reply_text(
                text_helper.usertext("language_show").format(
                    user.language, avaliable_languages
                )
            )
            return

        lang = lang[1]
        if lang not in avaliable_languages:
            await update.message.reply_text(
                text_helper.usertext("language_show").format(
                    user.language, avaliable_languages
                )
            )
            return

        self.bot.users[chat_id].language = lang
        self.bot.db.save_user(user)
        await update.message.reply_text(text_helper.usertext("language_set"))
