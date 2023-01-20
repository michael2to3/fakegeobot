from telethon import TelegramClient, events, types
from datetime import datetime
import asyncio
import time, os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
session_name = os.environ.get('SESSION_NAME')
bot_token = os.environ.get('BOT_TOKEN')

if api_id is None or api_hash is None or session_name is None or bot_token is None:
    print("Api is none")
    exit(1)

client = TelegramClient('session_name', int(api_id), api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond('Welcome! Please use /auth to authenticate')

@client.on(events.NewMessage(pattern='/auth'))
async def auth_handler(event):
    phone_number = event.message.text.split()[1]
    await client.send_code_request(phone_number)
    await event.respond("Code sent to your number")

    async def code_callback(event):
        code = event.message.text
        try:
            user_client = TelegramClient(phone_number, api_id, api_hash)
            await user_client.start(phone_number=phone_number, code=code)
            await event.respond('Authentication successful!')
            asyncio.create_task(send_location_task(user_client))
        except Exception as e:
            await event.respond('Error: ' + str(e))
        finally:
            client.remove_event_handler(code_callback, events.NewMessage)
    client.add_event_handler(code_callback, events.NewMessage)


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
        asyncio.create_task(send_location_task())

async def send_live_location(client):
    await client.send_message(
        '@me',
        file=types.InputMediaGeoLive(
            types.InputGeoPoint(59.965128, 30.398474),
            period=60
        )
    )
async def send_location_task():
    while True:
        # Send the live location to the specific username
        await send_live_location(client);
        await asyncio.sleep(1800) # 1800 seconds = 30 minutes


# Start the client
client.start(bot_token=bot_token)
client.run_until_disconnected()
