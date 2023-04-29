from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes


class Command(ABC):
    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        pass
