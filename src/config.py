from decouple import config


class Config:
    _api_id: int
    _bot_token: str
    _api_hash: str
    _session_name: str
    _auth_code: str

    def __init__(self):
        self._api_id = int(self._get_config('API_ID'))
        self._api_hash = self._get_config('API_HASH')
        self._session_name = self._get_config('SESSION_NAME')
        self._bot_token = self._get_config('BOT_TOKEN')

    def _get_config(self, name: str) -> str:
        output = config(name)
        if type(output) is str:
            return output
        raise Exception('Get varible form config is not found - ' + name)

    def get_api_id(self):
        return self._api_id

    def get_api_hash(self):
        return self._api_hash

    def get_session_name(self):
        return self._session_name

    def get_bot_token(self):
        return self._bot_token
