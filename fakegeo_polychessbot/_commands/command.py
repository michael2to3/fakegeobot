from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes
from bot import Bot


class Command(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    async def handle(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        pass
