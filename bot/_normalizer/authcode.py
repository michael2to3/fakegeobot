from .normalizer import Normalizer


class AuthCode(Normalizer):
    @staticmethod
    def normalize(text: str) -> str:
        code = text
        index_first_digit = [i.isdigit() for i in code].index(True)

        code = code[index_first_digit:].rstrip()
        code = AuthCode._bypass_protect_tg(code)

        has_not_allow_symbol = any(not i.isdigit() for i in code)
        if has_not_allow_symbol:
            raise ValueError("Auth code has not allow symbol")

        tg_len_code = 5
        if len(code) != tg_len_code:
            raise ValueError("Not correct code")

        return code

    @staticmethod
    def _bypass_protect_tg(text: str) -> str:
        return text.replace(".", "")
