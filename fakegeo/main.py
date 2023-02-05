from bot import Bot
from config import Config
import asyncio
from threading import Thread
import sys
import logging


def setup_logging():
    if '--debug' in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


def start_cron():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_bot():
    cnf = Config()
    bot = Bot(cnf._bot_token, cnf._api_id,
              cnf._api_hash, cnf._db_path, 'user.db')
    bot.run()


if __name__ == '__main__':
    setup_logging()
    tcron = Thread(target=start_cron)

    tcron.start()
    start_bot()

    tcron.join()
