import logging
from abc import ABC, abstractmethod

from ..abstract_bot import AbstractBot
from ..text import TextHelper
from telegram import Update
from telegram.ext import ContextTypes


class Command(ABC):
    def __init__(self, bot: AbstractBot, text_helper: TextHelper):
        self.logger = logging.getLogger(__name__)
        self.bot = bot
        self.text_helper = text_helper

    @abstractmethod
    async def handle(self, update: Update, _: ContextTypes) -> None:
        pass
