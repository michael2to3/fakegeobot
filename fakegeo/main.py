from bot import Bot
from config import Config

if __name__ == '__main__':
    config = Config()
    bot = Bot(config.bot_token,
              config.api_id, config.api_hash)
    bot.run()
