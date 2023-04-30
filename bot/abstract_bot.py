from abc import ABC, abstractmethod
from typing import Dict

from ._db import DatabaseHandler
from .model import ApiApp, User


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
