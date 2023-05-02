import gettext
import os
from typing import Dict
from ..model import User
from telegram import Update

locales_dir = os.path.join(os.path.dirname(__file__), "locales")


class Text:
    @staticmethod
    def langtext(text: str, language: str) -> str:
        lang = gettext.translation(
            "messages", locales_dir, languages=[language, "en"], fallback=True
        )
        return lang.gettext(text)

    @staticmethod
    def usertext(text: str, update: Update, users: Dict[int, User]) -> str:
        lang = Text._get_lang(update, users)
        return Text.langtext(text, lang)

    @staticmethod
    def _get_lang(update: Update, users: Dict[int, User]) -> str:
        chat_id = update.message.chat_id
        if chat_id in users:
            return users[chat_id].language
        else:
            language_code = update.message.from_user.language_code if update.message.from_user.language_code else "en"
            return language_code.split("_")[0]
