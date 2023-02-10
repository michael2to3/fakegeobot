![Poster](https://github.com/michael2to3/fakegeo-polychessbot/blob/main/.readme/poster.png)
# Telegram Fake Location Bot
A Python-based Telegram bot that allows users to send fake location data to other bots.
![Demo](https://github.com/michael2to3/fakegeo-polychessbot/blob/main/.readme/demo.mp4)

## Introduction
This bot was created to help users bypass location checks in various applications, such as lessons. It works by sending fake location data from the user to another bot. 

## Requirements
- Python 3.x
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [aiocron](https://github.com/gawel/aiocron)
- [python-decouple](https://github.com/HBNetwork/python-decouple)
- [Telethon](https://github.com/LonamiWebs/Telethon)

## Usage
1. Clone this repository
2. Run `pip install -r requirements.txt` to install required packages
3. Create a bot in Telegram and get your API key
4. Set your API key as an environment variable with the name `BOT_TOKEN`, `API_ID`, `API_HASH` and `SQLITE_PATH`
5. Run the bot using `python ./fakegeo/main.py`

## Start unit test

```sh
python -m unittest discover -s ./test/
```

## Contribution
Feel free to contribute to the project by submitting pull requests or opening issues for bug reports and feature requests.

## License
This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.
