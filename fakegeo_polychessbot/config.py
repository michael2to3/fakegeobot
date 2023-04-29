from decouple import config


class Config:
    _api_id: int
    _api_hash: str
    _bot_token: str
    _db_path: str

    def __init__(self):
        self._api_id = int(self._get_config("API_ID"))
        self._api_hash = self._get_config("API_HASH")
        self._bot_token = self._get_config("BOT_TOKEN")
        self._db_path = self._get_config("SQLITE_PATH")

    def __getattr__(self, name: str):
        return self.__dict__[name]

    def __setattr__(self, name: str, value):
        self.__dict__[name] = value

    def _get_config(self, name: str) -> str:
        output = config(name)
        if type(output) is str:
            return output
        raise Exception("Get varible form config is not found - " + name)
