import asyncio
import logging
import multiprocessing
import os
import sys

from bot import Bot
from _config import Config
from model import ApiApp
from _db import DatabaseHandler


def setup_logging():
    env_debug = os.environ.get("DEBUG", "false").lower()
    debug_flag = "--debug" in sys.argv or env_debug == "true"
    logging.basicConfig(level=logging.DEBUG if debug_flag else logging.WARN)


def get_root_path():
    root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, "..")


def generate_bot():
    cnf = Config()
    api = ApiApp(cnf.api_id, cnf.api_hash)
    db = DatabaseHandler(cnf.db_path, cnf.db_name)
    return Bot(api, cnf._bot_token, db)


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
    cron_process = multiprocessing.Process(target=start_cron)
    bot_process = multiprocessing.Process(target=start_bot)
    cron_process.start()
    bot_process.start()


if __name__ == "__main__":
    main()