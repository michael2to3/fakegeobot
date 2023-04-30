import logging
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes
from abstract_bot import AbstractBot


class Command(ABC):
    def __init__(self, bot: AbstractBot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    async def handle(self, update: Update, _: ContextTypes) -> None:
        pass
