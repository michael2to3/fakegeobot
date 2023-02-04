from bot import Bot
from config import Config
import asyncio
from threading import Thread


def start_cron():
    thread = Thread(target=asyncio.get_event_loop().run_forever)
    thread.start()


if __name__ == '__main__':
    start_cron()
    config = Config()
    bot = Bot(config.bot_token,
              config.api_id, config.api_hash)
    bot.run()
