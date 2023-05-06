import logging
from abc import ABC, abstractmethod

from ..bot import BotContext
from ..text import TextHelper
from telegram import Update
from telegram.ext import ContextTypes


class Command(ABC):
    def __init__(self, context: BotContext, text_helper: TextHelper):
        self.logger = logging.getLogger(__name__)
        self._context = context
        self.text_helper = text_helper

    @abstractmethod
    async def handle(self, update: Update, _: ContextTypes) -> None:
        pass
