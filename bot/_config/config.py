from dataclasses import dataclass
from decouple import config
from model import ApiApp


@dataclass
class Config:
    api: ApiApp
    bot_token: str
    db_path: str
    db_name: str
    cron_timeout: int

    def __post_init__(self):
        self.api = ApiApp(int(self._get_config("API_ID")), self._get_config("API_HASH"))
        self.bot_token = self._get_config("BOT_TOKEN")
        self.db_path = self._get_config("SQLITE_PATH")
        self.db_name = self._get_config("SQLITE_NAME")
        self.cron_timeout = int(self._get_config("CRON_TIMEOUT"))

    def _get_config(self, name: str) -> str:
        output = config(name)
        if isinstance(output, str):
            return output
        raise Exception("Get variable from config is not found - " + name)
