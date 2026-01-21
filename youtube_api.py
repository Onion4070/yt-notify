import os
from dotenv import load_dotenv
import aiohttp
import asyncio


load_dotenv('.env')
KEY = os.getenv('YOUTUBE_API_KEY')
VIDEO_ID = os.getenv('TEST_VIDEO_ID')


async def get_json(video_id: str):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics,snippet&id={video_id}&key={KEY}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return f'error: status code {response.status}'


async def get_live_status(video_id: str):
    res_json = await get_json(video_id)
    print(res_json)
    items = res_json['items']
    item  = items[0]
    live_status = res_json['items'][0]['snippet']['liveBroadcastContent']
    # live     -> 'live', 
    # upcoming -> 'upcoming'
    # else     -> 'none'
    return live_status


async def main():
    res_json = await get_json(VIDEO_ID)
    status = await get_live_status(VIDEO_ID)
    #print(res_json)
    #print(status)

if __name__ == '__main__':
    asyncio.run(main())
