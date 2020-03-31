def getContentLength(content: dict) -> str:
    try:
        return str(len("​id=%s&roomid=%s&type=%s&csrf_token=%s&csrf=%s&visit_id=" % (
            content.get('id'), content.get('roomid'), content.get('keyword'), content.get('csrf_token'), content.get('csrf')))-1)
    except:
        raise KeyError
        return "0"


def addRecordMsg(record: dict, roomid: str, msg: str, success=-1):
    try:
        if success != -1:
            record['score'] += success
        record.get('values').append(
            {'success': success, 'message': ("%s roomid=%s" % (msg, roomid))})
    except:
        raise KeyError


def createHeaders(userAgent: str, cookie: str):
    return {
        "Host": "api.live.bilibili.com",
        "User-Agent": userAgent,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "",
        "Origin": "https://live.bilibili.com",
        "Connection": "keep-alive",
        "Referer": "",
        "Cookie": cookie
    }


def getSearchMsg():
    return {
        "keyword": "正在抽奖",
        "targets": [
            {
                "name": "娱乐",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=sort_type_152&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "手游",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=sort_type_121&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "电台",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=5&cate_id=0&area_id=0&sort_type=sort_type_8&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "网游",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=sort_type_124&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "单机",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=6&cate_id=0&area_id=0&sort_type=sort_type_125&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "绘画",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=sort_type_56&page=%d&page_size=30&tag_version=1"
            }
        ]
    }
