from telethon import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.types import (
    PeerChannel,
    PeerUser,
    ReplyKeyboardMarkup,
    ReplyInlineMarkup,
    KeyboardButtonRow,
    KeyboardButton,
    KeyboardButtonUrl,
    KeyboardButtonCallback
)
from sql import DB
import configparser  # Library for reading from a configuration file, # pip install configparser
from datetime import date, timedelta

#### Access credentials
# config = configparser.ConfigParser() # Define the method to read the configuration file
# config.read('config.ini') # read config.ini file



# Create the client and the session called session_master. We start the session as the Bot (using bot_token)
client = TelegramClient('anon', api_id, api_hash).start(bot_token=BOT_TOKEN)


# Define the /start command
@client.on(events.NewMessage(pattern='/(?i)start'))
async def start(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = "Приветственное сообщение"
    file = '../result/speech/temp.ogg'
    keyboard_buttons = ReplyKeyboardMarkup(
        [
            KeyboardButtonRow(
                [
                    KeyboardButton(text="За эту неделю")
                ]
            )
        ]
    )
    # await client.send_file(SENDER, file, voice_note=False)
    await client.send_message(SENDER, text, buttons=keyboard_buttons)


@client.on(events.NewMessage(pattern='За эту неделю'))
async def week_news(event):
    sender = await event.get_sender()
    SENDER = sender.id
    text = 'Новости за неделю'

    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    data = db.select_rows_by_date(str(start_date), str(end_date))
    # file = '../result/speech/temp.ogg'
    await client.send_message(SENDER, text)
    for item in data:
        await client.send_file(SENDER, item, voice_note=True)


### First command, get the time and day
# @client.on(events.NewMessage(pattern='/(?i)time'))
# async def time(event):
#     # Get the sender of the message
#     sender = await event.get_sender()
#     SENDER = sender.id
#     text = "Received! Day and time: " + str(datetime.datetime.now())
#     await client.send_message(SENDER, text, parse_mode="HTML")


### MAIN
if __name__ == '__main__':
    db = DB()
    print("Bot Started!")
    client.run_until_disconnected()
