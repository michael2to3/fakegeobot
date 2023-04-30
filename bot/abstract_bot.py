from abc import ABC, abstractmethod
from typing import Dict
from model import ApiApp, User
from _db import DatabaseHandler


class AbstractBot(ABC):
    @abstractmethod
    def run(self):
        pass

    @property
    @abstractmethod
    def users(self) -> Dict[int, User]:
        pass

    @property
    @abstractmethod
    def db(self) -> DatabaseHandler:
        pass

    @property
    @abstractmethod
    def api(self) -> ApiApp:
        pass
