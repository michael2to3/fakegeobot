from decouple import config


class Config:
    __slots__ = ("_api_id", "_api_hash", "_bot_token", "_db_path", "_db_name")

    def __init__(self):
        self._api_id = int(self._get_config("API_ID"))
        self._api_hash = self._get_config("API_HASH")
        self._bot_token = self._get_config("BOT_TOKEN")
        self._db_path = self._get_config("SQLITE_PATH")
        self._db_name = self._get_config("SQLITE_NAME")

    def _get_config(self, name: str) -> str:
        output = config(name)
        if isinstance(output, str):
            return output
        raise Exception("Get variable from config is not found - " + name)

    @property
    def api_id(self):
        return self._api_id

    @property
    def api_hash(self):
        return self._api_hash

    @property
    def bot_token(self):
        return self._bot_token

    @property
    def db_path(self):
        return self._db_path

    @property
    def db_name(self):
        return self._db_name
