class Arg:
    def get_phone(self, text: str) -> str:
        parts = text.split()
        if parts is None or len(parts) != 2:
            raise ValueError('Not valid parse string')

        phone = parts[1]
        if phone is None or len(phone.strip()) == 0:
            raise ValueError('Not valid phone number')

        return phone

    def get_auth_code(self, text: str) -> int:
        parts = text.split()
        if parts is None or len(parts) > 1:
            raise ValueError('Not valid message')

        code = parts[0]
        if code is None or len(code.strip()) == 0:
            raise ValueError('Not valid auth code')

        tg_len_code = 5
        if len(code) != tg_len_code:
            raise ValueError('Not correct code')

        return int(code)
