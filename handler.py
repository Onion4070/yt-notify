import xml.etree.cElementTree as ET


def xml_parse(xml: bytes):
    # 名前空間の定義
    ## デフォルト: atom, 動画削除に関してはatの名前空間が利用される
    XML_NAMESPACE = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "at": "http://purl.org/atompub/tombstones/1.0",
    }

    root = ET.fromstring(xml)

    deleted_entry = root.find("at:deleted-entry", XML_NAMESPACE)
    entry = root.find("atom:entry", XML_NAMESPACE)

    if (deleted_entry is not None):
        return "Deleted Notify"

    title    = entry.find("atom:title",  XML_NAMESPACE)
    link     = entry.find("atom:link",   XML_NAMESPACE)
    author   = entry.find("atom:author", XML_NAMESPACE)
    video_id = entry.find("yt:videoId",  XML_NAMESPACE)

    name = author.find("atom:name", XML_NAMESPACE)
    uri  = author.find("atom:uri",  XML_NAMESPACE)

    print(f'title = {title.text}')
    print(f'name = {name.text}')
    print(f'uri = {uri.text}')
    return "Success"
