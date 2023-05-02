from .normalizer import Normalizer
import re


class PhoneNumber(Normalizer):
    @staticmethod
    def normalize(text: str) -> str:
        phone = PhoneNumber._remove_junk(text.strip())
        phone = re.sub(r"\D", "", phone)

        if len(phone) < 10 or len(phone) > 13:
            raise ValueError("Phone format is not valid")

        return f"+{phone}"

    @staticmethod
    def _remove_junk(utext: str) -> str:
        junk = [" ", "(", ")", "_"]
        for i in junk:
            utext = utext.replace(i, "")
        return utext
