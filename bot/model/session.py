class Session:
    def __init__(
        self,
        session_name: str,
        username: str,
        chat_id: int,
        phone: str | None,
        auth_code: int | None,
        phone_code_hash: str | None,
    ):
        self.session_name = session_name
        self.username = username
        self.chat_id = chat_id
        self.phone = phone
        self.auth_code = auth_code
        self.phone_code_hash = phone_code_hash

    @property
    def session_name(self) -> str:
        return self._session_name

    @session_name.setter
    def session_name(self, value: str):
        self._session_name = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def chat_id(self) -> int:
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value: int):
        self._chat_id = value

    @property
    def phone(self) -> str | None:
        return self._phone

    @phone.setter
    def phone(self, value: str | None):
        self._phone = value

    @property
    def auth_code(self) -> int | None:
        return self._auth_code

    @auth_code.setter
    def auth_code(self, value: int | None):
        self._auth_code = value

    @property
    def phone_code_hash(self) -> str | None:
        return self._phone_code_hash

    @phone_code_hash.setter
    def phone_code_hash(self, value: str | None):
        self._phone_code_hash = value

    def __str__(self) -> str:
        return f"Session({self.session_name}, {self.username}, {self.chat_id}, {self.phone}, {self.auth_code}, {self.phone_code_hash})"
