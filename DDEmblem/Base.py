import asyncio
import json
import time

import aiohttp
import async_timeout
# from fake_useragent import UserAgent


class Roster():
    """ 用于可抽奖直播间的信息检索和储存

    Members: 
        EventLoop:      事件循环。
        LiveRoomList:   储存抽奖直播间信息的列表，元素皆为一个字典，结构为：
            {
                'roomid': '...',            # 直播间id。
                'ruid': '...',              # 我也不知道这是什么，似乎是up主的id。
                'parent_id': '...'          # 大区所在id。
                'area_id': '...'            # 小分区id。
                'url': "https://xxx/..."    # 直播间链接。
            }
        Flags:          记录分区的最大页数，为一个字典。
        SearchMsg:      因为每个区的URL不尽相同，所以存储一个表示检索方式信息的字典，需满足以下结构：
            {
                "keyword": "XXXX",          # 检索关键词，通常为正在抽奖。
                "targets": [                # 检索目标的地址列表，一般为bilibili各直播大区。
                    {
                        "name": "xxx",
                        "url": "https://xxx/..."
                    },
                    {
                        "name": "yyy",
                        "url": "https://yyy/yyy/..."
                    }
                    # ...
                ]
            }

    Todo:   1、区分一个直播间的奖品是否已被成功领取。
            2、识别直播间中抽奖信息的数量和类型。
    """

    def __init__(self, searchMsg: dict):
        """ 构造器
        接收一个代表检索方式信息的字典作为参数，并建立空对象。

        Args:
            searchMsg: 描述检索方式的信息。

        Attention: 并不会对searchMsg的格式进行检索或抛出异常。
        """
        # self.UserAgent = UserAgent()
        self.LiveRoomList = []
        self.SearchMsg = searchMsg
        self.EventLoop = asyncio.get_event_loop()
        self.Flags = dict(
            zip([d['name'] for d in self.SearchMsg['targets']], len(self.SearchMsg['targets'])*[1000]))

    def Loads(self, basePage=1, topPage=3) -> str:
        """ 加载容器内容的函数
        函数解析SearchMsg的内容，并按页面（即30个直播间一组）来分配任务列表到事件循环中。

        Args:
            headers:    HTTP请求头，本函数中可为空。
            basePage:   从哪一页开始读取。
            topPage:    最大读取到哪一页。

        Returns:
            无返回值。

        Raises:
            ValueError: 
                页数过多时可能会导致此错误，
                原因为asyncio调用的select()的打开文件数有限。
            KeyError: SearchMsg的内容有误时抛出。
            RosterRangeError: 未实现，当topPage低于basePage时抛出。
        """
        continueable = False
        try:
            keyWord = self.SearchMsg.get('keyword')
            targets = self.SearchMsg.get('targets')
        except:
            raise KeyError
        taskList = []
        for target in targets:
            maxPage = self.Flags.get(target.get('name'))
            for page in range(basePage, topPage+1):
                if page <= maxPage:
                    taskList.append(self.EventLoop.create_task(
                        self.LoadPage(target, page, keyWord)))
                else:
                    pass
        if len(taskList) != 0:
            self.EventLoop.run_until_complete(asyncio.wait(taskList))

    def LoadAll(self, step=50):
        continueable = True
        page = 1
        while continueable:
            for key in self.Flags:
                continueable = continueable and (page >= self.Flags[key])
            continueable = not continueable
            self.Loads(basePage=page, topPage=page+step)
            page = page+step+1

    def Push(self, roomId: str, ruId: str, parentId: str, areaId: str, url: str) -> dict:
        dic = {
            'roomid': roomId,
            'ruid': ruId,
            'parent_id': parentId,
            'area_id': areaId,
            'url': url
        }
        self.LiveRoomList.append(dic)
        return dic

    async def LoadPage(self, target: dict, page: int, keyWord: str):
        response = {}
        try:
            url = target.get('url') % (page)
        except:
            raise KeyError
        # headers = {'User-Agent': self.UserAgent.random}
        headers = None
        try:
            with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as res:
                        # 请求成功则拉取Json报文。
                        if res.status == 200:
                            response = json.loads(await res.text())
                        else:
                            return False
        except asyncio.TimeoutError as e:
            return False
        roomList = response.get('data').get('list')
        # 如果超过了最大页数，接收的roomList的长度则为0。
        if len(roomList) == 0:
            self.Flags[target.get('name')] = min(
                page, self.Flags[target.get('name')])
            return False
        # 如果显示正在抽奖的关键字，则读取直播间信息，并根据直播间ID生成链接。
        for roomData in roomList:
            try:
                if roomData.get('pendant_info').get('2').get('content') == keyWord:
                    self.LiveRoomList.append({
                        'roomid': roomData.get('roomid'),
                        'ruid': roomData.get('uid'),
                        'parent_id': roomData.get('parent_id'),
                        'area_id': roomData.get('area_id'),
                        'url': "https://live.bilibili.com%s" % (roomData.get('link'))
                    })
                else:
                    continue
            except:
                continue
        return True


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
            {'roomid': roomid, 'success': success, 'message': msg})
    except:
        raise KeyError


def log(file, score: int, roomid: str, msg: str, success=0):
    if file == None:
        return
    try:
        print("{0:<10}    RoomID: {1:<10} Result: {2:<5} Message: {3:<10}".format(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), roomid, success, msg), file=file)
    except:
        raise KeyError


def createHeaders(cookie: str):
    return {
        "Host": "api.live.bilibili.com",
        "User-Agent": "",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "",
        "Origin": "https://live.bilibili.com",
        # "Connection": "keep-alive",
        "Referer": "",
        "Cookie": cookie
    }


def getSearchMsg():
    ''' 返回可以用于构筑Base.Roster的检索信息
    因为B站各大分区getRoomList接口的URL有着细微的差别，不排除会有改变的可能，所以这里将它独立出来作为一个字典信息。

    Return: 检索信息字典。
    '''
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
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=6&cate_id=0&area_id=0&sort_type=sort_type_150&page=%d&page_size=30&tag_version=1"
            },
            {
                "name": "绘画",
                "url": "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=sort_type_56&page=%d&page_size=30&tag_version=1"
            }
        ]
    }
