import os
import polib
from typing import Dict
from ..model import User
from telegram import Update


class TextHelper:
    _cache = {}

    def __init__(self, update: Update, users: Dict[int, User]):
        self.chat_id = update.message.chat_id
        self.from_user = update.message.from_user
        self.users = users

    def usertext(self, text: str) -> str:
        localedir = os.path.join(os.path.dirname(__file__), "..", "locales")
        lang = self._get_lang()

        if lang not in TextHelper._cache:
            po_filepath = os.path.join(localedir, lang, "LC_MESSAGES", "messages.po")
            TextHelper._cache[lang] = polib.pofile(po_filepath)

        po = TextHelper._cache[lang]
        entry = po.find(text)
        if entry and entry.msgstr:
            return entry.msgstr
        else:
            return text

    def _get_lang(self) -> str:
        if self.chat_id in self.users:
            return self.users[self.chat_id].language
        else:
            language_code = (
                self.from_user.language_code if self.from_user.language_code else "en"
            )
            return language_code.split("_")[0]
