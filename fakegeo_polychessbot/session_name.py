from random import choice

import hashlib


class SessionName:
    _length: int
    _allow_char: str

    def __init__(self):
        self._length = 64
        allow_digit = self._get_range_str('0', '9')
        allow_lowcase = self._get_range_str('a', 'z')
        allow_uppercase = self._get_range_str('A', 'Z')
        self._allow_char = allow_digit + allow_lowcase + allow_uppercase

    def _get_range_str(self, lhs: str, rhs: str) -> str:
        return ''.join(map(chr, range(ord(lhs), ord(rhs) + 1)))

    def _get_random_char(self) -> str:
        return choice(self._allow_char)

    def _get_md5(self, text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def get_session_name_base(self, base: str) -> str:
        return self._get_md5(base)

    def get_session_name(self):
        union_name = ''
        for _ in range(self._length):
            union_name += self._get_random_char()
        postfix = '.session'
        return union_name + postfix
