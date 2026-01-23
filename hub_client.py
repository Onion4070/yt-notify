import os
from dotenv import load_dotenv
import asyncio
import aiohttp


load_dotenv('.env')

hub_url = 'https://pubsubhubbub.appspot.com/subscribe'
callback_url = os.getenv('CALLBACK_URL')


async def subscribe(channel_id: str):
    topic_url = f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}'

    header = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'hub.callback': callback_url, 
        'hub.mode': 'subscribe', 
        'hub.topic': topic_url, 
        'hub.verify': 'async', 
        'hub.lease_seconds': 864000, # 10日 
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hub_url, data=params, headers=header) as res:
            return res


async def unsubscribe(channel_id: str):
    topic_url = f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}'

    header = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'hub.callback': callback_url, 
        'hub.mode': 'unsubscribe', 
        'hub.topic': topic_url, 
        'hub.verify': 'async', 
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hub_url, data=params, headers=header) as res:
            return res

 
async def main():
    channel_id = os.getenv('TEST_CHANNEL_ID')
    res = await subscribe(channel_id)
    print(res)


if __name__ == '__main__':
    asyncio.run(main())

