import os
from dotenv import load_dotenv
from datetime import datetime
import requests as req

load_dotenv('.env')
KEY = os.getenv('YOUTUBE_API_KEY')


def get(video_id: str):
    URL = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,statistics,snippet&id={video_id}&key={KEY}'
    res = req.get(URL).json()
    return res

if __name__ == '__main__':
    print(get(os.getenv('TEST_VIDEO_ID')))
