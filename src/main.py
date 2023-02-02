from bot import Bot
from config import Config
import asyncio

if __name__ == '__main__':
    config = Config()
    bot = Bot(config.get_bot_token())
    asyncio.run(bot.run())
