from dataclasses import dataclass
import xml.etree.cElementTree as ET
from datetime import datetime
from dateutil.parser import parse
from dateutil.tz import gettz

@dataclass(frozen=True)
class VideoData:
    title: str
    link: str
    video_id: str
    name: str
    channel_uri: str
    published: datetime
    updated: datetime


def xml_parse(xml: bytes):
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
            updated
        )

    # 通常の通知
    entry = root.find('atom:entry', XML_NAMESPACE)

    title     = entry.find('atom:title',  XML_NAMESPACE).text
    link      = entry.find('atom:link',   XML_NAMESPACE).get('href')
    author    = entry.find('atom:author', XML_NAMESPACE)
    video_id  = entry.find('yt:videoId',  XML_NAMESPACE).text
    published = parse(entry.find('atom:published', XML_NAMESPACE).text).astimezone(gettz('Asia/Tokyo'))
    updated   = parse(entry.find('atom:updated', XML_NAMESPACE).text).astimezone(gettz('Asia/Tokyo'))

    name = author.find('atom:name', XML_NAMESPACE).text
    channel_uri  = author.find('atom:uri',  XML_NAMESPACE).text

    return VideoData(
        title, 
        link, 
        video_id, 
        name, 
        channel_uri, 
        published, 
        updated
    )
