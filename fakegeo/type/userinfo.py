class UserInfo:
    _session_name: str
    _username: str
    _chat_id: int
    _phone: str
    _auth_code: int
    _schedule: str

    def __init__(
            self,
            session_name: str,
            username: str,
            chat_id: int,
            phone: str,
            auth_code: int,
            schedule: str = '30 18 * * 5'):
        self._session_name = session_name
        self._username = username
        self._chat_id = chat_id
        self._phone = phone
        self._auth_code = auth_code
        self._schedule = schedule  # Default value: At 6:30pm on Friday

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value
