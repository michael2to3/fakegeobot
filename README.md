# Telegram Fake Location Bot

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/michael2to3/fakegeo-polychessbot)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/b5916201dffd4ffeb04e52fd30172812)](https://app.codacy.com/gh/michael2to3/fakegeo-polychessbot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/b5916201dffd4ffeb04e52fd30172812)](https://app.codacy.com/gh/michael2to3/fakegeo-polychessbot/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

![Poster](https://github.com/michael2to3/fakegeo-polychessbot/blob/main/.readme/poster.png)
A Python-based Telegram bot that allows users to send fake location data to other bots.

https://user-images.githubusercontent.com/87614587/218004599-2d3e04d4-e8f4-42bd-83d0-cd6e30af56b9.mp4

## Introduction
This bot was created to help users bypass location checks in various applications, such as lessons. It works by sending fake location data from the user to another bot.
*⚠️ Warning*: By creating an authentication session, you are granting this bot full access to your Telegram account. This includes the ability to read your messages, send messages on your behalf, and manage your account. Please ensure you trust the bot and its developers before proceeding. If you have any concerns, please review the bot's source code or contact the developers directly.

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

```bash
python -m unittest discover -s ./test/
```

## Contribution
Feel free to contribute to the project by submitting pull requests or opening issues for bug reports and feature requests.

## License
This project is licensed under the GNU License. See the [LICENSE](https://github.com/michael2to3/fakegeo-polychessbot/blob/main/.readme/LICENSE) file for more information.
