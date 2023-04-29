from _normalizer import Normalizer


class PhoneNumber(Normalizer):
    _phonenumber: str

    def __init__(self, phonenumber: str):
        self._phonenumber = phonenumber

    def normalize(self, text: str) -> str:
        phone = self._remove_junk(text)

        index_first_digit = [i.isdigit() for i in phone].index(True)
        has_plus = phone[index_first_digit - 1] == "+"

        phone = phone[index_first_digit:].rstrip()

        has_not_allow_symbol = any(not i.isdigit() for i in phone)
        if has_not_allow_symbol:
            raise ValueError("Phone number has not allow symbol")

        if len(phone) < 10 or len(phone) > 13:
            raise ValueError("Phone format is not valid")

        preffix = "+" if has_plus else ""
        return preffix + phone

    def _remove_junk(self, utext: str) -> str:
        junk = [" ", "(", ")", "_"]
        for i in junk:
            utext = utext.replace(i, "")
        return utext
