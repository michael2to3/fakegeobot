from dataclasses import dataclass, field

from decouple import config
from ..model import ApiApp, Geolocation


@dataclass
class Config:
    api_id: int = field(init=False)
    api_hash: str = field(init=False)
    bot_token: str = field(init=False)
    db_uri: str = field(init=False)
    cron_timeout: int = field(init=False)
    cron_expression: str = field(init=False)
    location_interval: int = field(init=False)
    location: Geolocation = field(init=False)
    recipient: str = field(init=False)

    def __post_init__(self):
        self.api = ApiApp(int(self._get_config("API_ID")), self._get_config("API_HASH"))
        self.bot_token = self._get_config("BOT_TOKEN")
        self.db_uri = self._get_config("DB_URI")
        self.cron_timeout = int(self._get_config("CRON_TIMEOUT"))
        self.cron_expression = self._get_config("CRON_EXPRESSION")
        self.location_interval = int(self._get_config("LOCATION_INTERVAL"))
        self.location = Geolocation(
            lat=float(self._get_config("LOCATION_LAT")),
            long=float(self._get_config("LOCATION_LONG")),
            interval=int(self._get_config("LOCATION_INTERVAL")),
        )
        self.recipient = self._get_config("RECIPIENT")

    def _get_config(self, name: str) -> str:
        output = config(name)
        if isinstance(output, str):
            return output
        raise Exception("Get variable from config is not found - " + name)
