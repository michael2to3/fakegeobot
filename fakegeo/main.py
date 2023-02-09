from bot import Bot
import os
from config import Config
from type import Api
import asyncio
from threading import Thread
import sys
import logging
from decouple import config
import nest_asyncio

nest_asyncio.apply()


def setup_logging():
    if '--debug' in sys.argv or config('DEBUG') == 'true':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


def get_root_path():
    root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, '..')


def generate_bot():
    root = get_root_path()
    cnf = Config()
    api = Api(cnf._api_id, cnf._api_hash)
    bot = Bot(api, cnf._bot_token,  os.path.join(
        root, cnf._db_path), 'user.db')
    return bot


def start_bot():
    bot = generate_bot()
    bot.run()


def worker(ws, loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ws())


def start_cron():
    run = asyncio.get_event_loop().run_forever
    loop = asyncio.new_event_loop()
    thread = Thread(target=worker, args=(run, loop,))
    thread.start()


async def main():
    setup_logging()
    start_cron()
    start_bot()

if __name__ == '__main__':
    asyncio.run(main())
