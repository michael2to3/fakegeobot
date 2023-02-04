from bot import Bot
from config import Config
import asyncio
from threading import Thread


def start_cron():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_bot():
    config = Config()
    bot = Bot(config.bot_token,
              config.api_id, config.api_hash)
    bot.run()


if __name__ == '__main__':
    tcron = Thread(target=start_cron)

    tcron.start()
    start_bot()

    tcron.join()
