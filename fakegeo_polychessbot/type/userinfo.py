class UserInfo:
    def __init__(
        self,
        session_name: str,
        username: str,
        chat_id: int,
        phone: str,
        auth_code: int,
        schedule: str,
        phone_code_hash: str,
    ):
        self.session_name = session_name
        self.username = username
        self.chat_id = chat_id
        self.phone = phone
        self.auth_code = auth_code
        self.schedule = schedule
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
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    @property
    def auth_code(self) -> int:
        return self._auth_code

    @auth_code.setter
    def auth_code(self, value: int):
        self._auth_code = value

    @property
    def schedule(self) -> str:
        return self._schedule

    @schedule.setter
    def schedule(self, value: str):
        self._schedule = value

    @property
    def phone_code_hash(self) -> str:
        return self._phone_code_hash

    @phone_code_hash.setter
    def phone_code_hash(self, value: str):
        self._phone_code_hash = value
