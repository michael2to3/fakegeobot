from decouple import config


class Config:
    _api_id: int
    _bot_token: str
    _api_hash: str
    _auth_code: str

    def __init__(self):
        self.api_id = int(self._get_config('API_ID'))
        self.api_hash = self._get_config('API_HASH')
        self.bot_token = self._get_config('BOT_TOKEN')

    def __getattr__(self, name: str):
        return self.__dict__[f'_{name}']

    def __setattr__(self, name: str, value):
        self.__dict__[f'_{name}'] = value

    def _get_config(self, name: str) -> str:
        output = config(name)
        if type(output) is str:
            return output
        raise Exception('Get varible form config is not found - ' + name)
