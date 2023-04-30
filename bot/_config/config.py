from dataclasses import dataclass, field

from decouple import config
from ..model import ApiApp


@dataclass
class Config:
    api_id: int = field(init=False)
    api_hash: str = field(init=False)
    bot_token: str = field(init=False)
    db_path: str = field(init=False)
    db_name: str = field(init=False)
    cron_timeout: int = field(init=False)
    location_interval: int = field(init=False)

    def __post_init__(self):
        self.api = ApiApp(int(self._get_config("API_ID")), self._get_config("API_HASH"))
        self.bot_token = self._get_config("BOT_TOKEN")
        self.db_path = self._get_config("SQLITE_PATH")
        self.db_name = self._get_config("SQLITE_NAME")
        self.cron_timeout = int(self._get_config("CRON_TIMEOUT"))
        self.location_interval = int(self._get_config("LOCATION_INTERVAL"))

    def _get_config(self, name: str) -> str:
        output = config(name)
        if isinstance(output, str):
            return output
        raise Exception("Get variable from config is not found - " + name)
