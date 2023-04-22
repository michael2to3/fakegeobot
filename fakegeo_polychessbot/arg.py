import logging


class Arg:
    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_phone(self, text: str) -> str:
        def remove_junk(utext: str) -> str:
            junk = [" ", "(", ")", "_"]
            for i in junk:
                utext = utext.replace(i, "")
            return utext

        phone = remove_junk(text)

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

    def get_auth_code(self, text: str) -> int:
        code = text
        index_first_digit = [i.isdigit() for i in code].index(True)

        code = code[index_first_digit:].rstrip()
        code = self.bypass_protect_tg(code)

        has_not_allow_symbol = any(not i.isdigit() for i in code)
        if has_not_allow_symbol:
            raise ValueError("Auth code has not allow symbol")

        tg_len_code = 5
        if len(code) != tg_len_code:
            raise ValueError("Not correct code")

        return int(code)

    def bypass_protect_tg(self, text: str) -> str:
        return text.replace(".", "")

    def get_cron(self, text: str) -> str:
        has_cmd = text.lstrip()[0] == "/"
        sch = text
        if has_cmd:
            findex = text.find(" ")
            sch = text[findex + 1 :]
        if len(sch) < 9:
            raise ValueError("Not valid format of cron")
        return sch
