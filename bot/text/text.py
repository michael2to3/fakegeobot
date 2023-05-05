import os
import polib
from typing import Dict
from ..model import User
from telegram import Update


class Text:
    _cache = {}

    @staticmethod
    def usertext(text: str, update: Update, users: Dict[int, User]) -> str:
        localedir = os.path.join(os.path.dirname(__file__), "..", "locales")
        lang = Text._get_lang(update, users)

        if lang not in Text._cache:
            po_filepath = os.path.join(localedir, lang, "LC_MESSAGES", "messages.po")
            Text._cache[lang] = polib.pofile(po_filepath)

        po = Text._cache[lang]
        entry = po.find(text)
        if entry and entry.msgstr:
            return entry.msgstr
        else:
            return text

    @staticmethod
    def _get_lang(update: Update, users: Dict[int, User]) -> str:
        chat_id = update.message.chat_id
        if chat_id in users:
            return users[chat_id].language
        else:
            language_code = (
                update.message.from_user.language_code
                if update.message.from_user.language_code
                else "en"
            )
            return language_code.split("_")[0]
