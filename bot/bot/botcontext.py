from .._config import Config
from .._db import DatabaseHandler
from ..model import ApiApp, User
from typing import Dict


class BotContext:
    def __init__(
        self, api: ApiApp, users: Dict[int, User], db: DatabaseHandler, config: Config
    ):
        self.api = api
        self.users = users
        self.db = db
        self.config = config
