import os
from dotenv import load_dotenv
from datetime import datetime
import requests as req


load_dotenv('.env')
KEY = os.getenv('YOUTUBE_API_KEY')


def get_json(video_id: str):
    URL = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics,snippet&id={video_id}&key={KEY}'
    res_json = req.get(URL).json()
    return res_json


def get_live_status(video_id: str):
    res_json = get_json(video_id)
    live_status = res_json['items'][0]['snippet']['liveBroadcastContent']
    # live     -> 'live', 
    # upcoming -> 'upcoming'
    # else     -> 'none'
    return live_status 


if __name__ == '__main__':
    print(get_live_status(os.getenv('TEST_VIDEO_ID')))
