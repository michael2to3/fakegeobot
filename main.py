from telethon import TelegramClient, events, types
from datetime import datetime
import schedule
import time, os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
session_name = os.environ.get('SESSION_NAME')
bot_token = os.environ.get('BOT_TOKEN')

if api_id is None or api_hash is None or session_name is None or bot_token is None:
    print("Api is none")
    exit(1)

# Create a new Telegram client
client = TelegramClient('session_name', int(api_id), api_hash)

# Start the client
client.start(bot_token=bot_token)

# Handle the '/start' command
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond('Welcome! Please use /auth to authenticate')

# Handle the '/auth' command
@client.on(events.NewMessage(pattern='/auth'))
async def auth_handler(event):
    # Send the Telegram Login Widget
    await event.respond('Please click on this link to authenticate: t.me/your_bot?start=auth_token')

# Handle the callback from the Telegram Login Widget
@client.on(events.CallbackQuery(data='auth_token'))
async def auth_callback_handler(event):
    # Get the phone number and code from the callback
    phone_number = event.message.message.phone_number
    code = event.message.message.code
    # Try to complete the authentication
    try:
        await client.sign_in(phone_number, code)
    except Exception as e:
        await event.respond('Error: ' + str(e))
    else:
        await event.respond('Authentication successful!')
        # Schedule the job to send live location every 30 minutes
        schedule.every(30).minutes.do(send_location)

async def send_location():
    await client.send_message(
        '@me',
        file=types.InputMediaGeoLive(
            types.InputGeoPoint(59.965128, 30.398474),
            period=60
        )
    )



while True:
    schedule.run_pending()
    time.sleep(1)

# Stop the client
client.stop()

