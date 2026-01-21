import asyncio
import os
from dataclasses import dataclass
from enum import Enum
import xml.etree.cElementTree as ET
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz

import youtube_api

class VideoStatus(Enum):
    VIDEO    = 'video'
    SHORT    = 'short'
    LIVE     = 'live'
    UPCOMING = 'upcoming'
    DELETED  = 'deleted'


@dataclass(frozen=True)
class VideoData:
    title: str
    link: str
    video_id: str
    name: str
    channel_uri: str
    published: datetime
    updated: datetime
    status: VideoStatus


async def xml_parse(xml: bytes):
    # 名前空間の定義
    ## デフォルト: atom, 動画削除に関してはatの名前空間が利用される
    XML_NAMESPACE = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'at': 'http://purl.org/atompub/tombstones/1.0',
    }

    root = ET.fromstring(xml)

    # 動画削除通知は例外処理
    deleted_entry = root.find('at:deleted-entry', XML_NAMESPACE)
    if (deleted_entry is not None):
        title = 'Unknown'
        link = deleted_entry.find('atom:link', XML_NAMESPACE).get('href')
        video_id = deleted_entry.get('ref')
       
        by = deleted_entry.find('at:by', XML_NAMESPACE)
        name = by.find('atom:name', XML_NAMESPACE).text
        channel_uri = by.find('atom:uri', XML_NAMESPACE).text
        updated = parse(deleted_entry.get('when')).astimezone(gettz('Asia/Tokyo'))
        published = updated

        return VideoData(
            title, 
            link, 
            video_id, 
            name, 
            channel_uri, 
            published, 
            updated, 
            status=VideoStatus.DELETED
        )

    # 通常の通知
    print('normal entry')
    entry = root.find('atom:entry', XML_NAMESPACE)

    title     = entry.find('atom:title',  XML_NAMESPACE).text
    link      = entry.find('atom:link',   XML_NAMESPACE).get('href')
    author    = entry.find('atom:author', XML_NAMESPACE)
    video_id  = entry.find('yt:videoId',  XML_NAMESPACE).text
    published = parse(entry.find('atom:published', XML_NAMESPACE).text).astimezone(gettz('Asia/Tokyo'))
    updated   = parse(entry.find('atom:updated', XML_NAMESPACE).text).astimezone(gettz('Asia/Tokyo'))

    name = author.find('atom:name', XML_NAMESPACE).text
    channel_uri  = author.find('atom:uri',  XML_NAMESPACE).text

    live_status = await youtube_api.get_live_status(video_id)
    print(f'live status = {live_status}')

    # デフォルト値は通常動画
    status = VideoStatus.VIDEO

    # 各種状態判定
    if ('/shorts' in link):
        status = VideoStatus.SHORT
    elif (live_status == 'upcoming'):
        status = VideoStatus.UPCOMING
    elif (live_status == 'live'):
        status = VideoStatus.LIVE
    
    return VideoData(
        title, 
        link, 
        video_id, 
        name, 
        channel_uri, 
        published, 
        updated,
        status
    ) 


async def main():
    xml = b"""<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
    <link rel="hub" href="https://pubsubhubbub.appspot.com" />
    <link rel="self"
        href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCnnL8tPKzfrHnbkWJtXY0wg" />
    <title>YouTube video feed</title>
    <updated>2026-01-19T02:39:48.809894593+00:00</updated>
    <entry>
        <id>yt:video:9t18yl0NwGo</id>
        <yt:videoId>9t18yl0NwGo</yt:videoId>
        <yt:channelId>UCnnL8tPKzfrHnbkWJtXY0wg</yt:channelId>
        <title>test</title>
        <link rel="alternate" href="https://www.youtube.com/shorts/9t18yl0NwGo" />
        <author>
            <name>maybeOnion</name>
            <uri>https://www.youtube.com/channel/UCnnL8tPKzfrHnbkWJtXY0wg</uri>
        </author>
        <published>2026-01-19T01:54:47+00:00</published>
        <updated>2026-01-19T02:39:48.809894593+00:00</updated>
    </entry>
</feed>
"""
    data = await xml_parse(xml)


if __name__ == '__main__':
    asyncio.run(main())
