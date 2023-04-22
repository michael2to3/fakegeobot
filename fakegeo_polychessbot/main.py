import asyncio
import logging
import multiprocessing
import os
import sys

from bot import Bot
from config import Config
from decouple import config
from type import Api


def setup_logging():
    envDebug = "false"
    try:
        envDebug = config("DEBUG")
    except Exception:
        envDebug = "false"

    if "--debug" in sys.argv or envDebug == "true":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


def get_root_path():
    root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, "..")


def generate_bot():
    root = get_root_path()
    cnf = Config()
    api = Api(cnf._api_id, cnf._api_hash)
    bot = Bot(api, cnf._bot_token, os.path.join(root, cnf._db_path), "user.db")
    return bot


def start_bot():
    bot = generate_bot()
    bot.run()


def start_cron():
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()


def main():
    setup_logging()
    p1 = multiprocessing.Process(target=start_cron)
    p2 = multiprocessing.Process(target=start_bot)
    p1.start()
    p2.start()


if __name__ == "__main__":
    main()
