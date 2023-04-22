# Telegram Fake Location Bot

[![Code Style](https://img.shields.io/badge/code%20style-pep8-orange)](https://www.python.org/dev/peps/pep-0008/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b5916201dffd4ffeb04e52fd30172812)](https://app.codacy.com/gh/michael2to3/fakegeo-polychessbot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

![Poster](https://github.com/michael2to3/fakegeo-polychessbot/blob/main/.readme/poster.png)
A Python-based Telegram bot that allows users to send fake location data to other bots.

https://user-images.githubusercontent.com/87614587/218004599-2d3e04d4-e8f4-42bd-83d0-cd6e30af56b9.mp4

## Introduction
This bot was created to help users bypass location checks in various applications, such as lessons. It works by sending fake location data from the user to another bot. 

## Requirements
- Python 3.x
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [aiocron](https://github.com/gawel/aiocron)
- [python-decouple](https://github.com/HBNetwork/python-decouple)
- [Telethon](https://github.com/LonamiWebs/Telethon)


## Telegram API
- You need to create an API client to use this script. You can do it by following these steps:
  1. Go to [my.telegram.org](https://my.telegram.org/)
  2. Log in using your Telegram account
  3. Click on `API Development Tools`
  4. Fill in the required fields and create your API client
  5. Replace `YOUR_API_ID` and `YOUR_API_HASH` in the `docker-copose.yml` or `main.py`

## Usage
1. Clone this repository
2. Run `pip install -r requirements.txt` to install required packages
3. Create a bot in Telegram and get your API key
4. Set your API key as an environment variable with the name `BOT_TOKEN`, `API_ID`, `API_HASH` and `SQLITE_PATH`
5. Run the bot using `python ./fakegeo/main.py`

## Docker
- Build the container using the command `docker build -t your_image_name .`
- Run the container using the command `docker run your_image_name`

## Docker compose
- Run with docker compose using the command `docker-compose up -d --build`

## Start unit test

```sh
python -m unittest discover -s ./test/
```

## To-do
- [ ] Switch to telethon for bot SDK
- [ ] Remove duplicate functional
- [ ] Disable from cron event too frequent handling
- [ ] Send telegram after delete session

## Contribution
Feel free to contribute to the project by submitting pull requests or opening issues for bug reports and feature requests.

## License
This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.
