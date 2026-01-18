import os
import requests as req
import json
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN      = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

def notify(msg):
    header = {
        'authorization':f'Bot {TOKEN}', 
        'content-type':'application/json'
    }

    payload = {'content':msg}
    payload = json.dumps(payload)

    url = f'https://discordapp.com/api/channels/{CHANNEL_ID}/messages'
    req.post(url, data=payload, headers=header)

if __name__ == '__main__':
    notify("Hello World")
