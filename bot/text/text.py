import gettext
from abc import abstractmethod
import os


locales_dir = os.path.join(os.path.dirname(__file__), "locales")


def usertext(cls, text: str, language: str) -> str:
    lang = gettext.translation(
        "messages", locales_dir, languages=[language, "en"], fallback=True
    )
    return lang.gettext(text)
