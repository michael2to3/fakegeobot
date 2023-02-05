import logging


class Arg:
    logger: logging.Logger

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_phone(self, text: str) -> str:
        self.logger.debug('Get phone from string', text)

        def remove_junk(utext: str) -> str:
            junk = [' ', '(', ')', '_']
            for i in junk:
                utext = utext.replace(i, '')
            return utext

        phone = remove_junk(text)

        index_first_digit = [i.isdigit() for i in phone].index(True)
        has_plus = phone[index_first_digit - 1] == '+'

        phone = phone[index_first_digit:].rstrip()

        has_not_allow_symbol = any(not i.isdigit() for i in phone)
        if has_not_allow_symbol:
            raise ValueError('Phone number has not allow symbol')

        if len(phone) < 10 or len(phone) > 13:
            raise ValueError('Phone format is not valid')

        preffix = '+' if has_plus else ''
        return preffix + phone

    def get_auth_code(self, text: str) -> int:
        self.logger.debug('Get auth code from string', text)

        code = text
        index_first_digit = [i.isdigit() for i in code].index(True)

        code = code[index_first_digit:].rstrip()

        has_not_allow_symbol = any(not i.isdigit() for i in code)
        if has_not_allow_symbol:
            raise ValueError('Auth code has not allow symbol')

        tg_len_code = 5
        if len(code) != tg_len_code:
            raise ValueError('Not correct code')

        return int(code)
