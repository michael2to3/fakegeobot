from bot import Bot
from config import Config
from type import Api
import asyncio
from threading import Thread
import sys
import logging
from decouple import config


def setup_logging():
    if '--debug' in sys.argv or config('DEBUG') == 'true':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


def start_cron():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()


def start_bot():
    cnf = Config()
    api = Api(cnf._api_id, cnf._api_hash)
    bot = Bot(api, cnf._bot_token,  cnf._db_path, 'user.db')
    bot.run()


if __name__ == '__main__':
    setup_logging()
    tcron = Thread(target=start_cron)

    tcron.start()
    start_bot()

    tcron.join()
