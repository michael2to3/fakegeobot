import hashlib
import secrets
import string


class SessionName:
    _length: int
    _allow_char: str

    def __init__(self):
        self._length = 64
        self._allow_char = string.ascii_letters + string.digits

    def _get_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get_session_name_base(self, base: str) -> str:
        return self._get_hash(base)

    def get_session_name(self) -> str:
        union_name = "".join(
            secrets.choice(self._allow_char) for _ in range(self._length)
        )
        postfix = ".session"
        return union_name + postfix
