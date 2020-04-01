import asyncio
import json

import aiohttp


class Roster:
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
        SearchMsg:      检索方式信息。 

    Todo: 1、区分一个直播间的奖品是否已被成功领取。
            2、识别直播间中抽奖信息的数量和类型。
    """

    def __init__(self, searchMsg: dict):
        """ 构造器
        接收一个代表检索方式信息的字典作为参数，并建立空对象。

        Args:
            searchMsg: 描述检索方式的信息，应为一个字典，可通过SearchMsg.json转化所得，并满足以下结构：
                {
                    "keyword": "正在抽奖",  # 检索关键词，通常为正在抽奖。
                    "targets": [    # 检索目标的地址列表，一般为bilibili各直播大区。
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

        Attention: 并不会对searchMsg的格式进行检索或抛出异常。
        """
        self.LiveRoomList = []
        self.SearchMsg = searchMsg
        self.EventLoop = asyncio.get_event_loop()
        self.Flags = dict(
            zip([d['name'] for d in self.SearchMsg['targets']], len(self.SearchMsg['targets'])*[1000]))

    def Loads(self, basePage=1, topPage=3, headers=None) -> str:
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
        # 循环构筑协程
        taskList = []
        for target in targets:
            maxPage = self.Flags.get(target.get('name'))
            for page in range(basePage, topPage+1):
                if page <= maxPage:
                    taskList.append(self.EventLoop.create_task(
                        self.LoadPage(target, page, keyWord, headers)))
                else:
                    pass
        if len(taskList) != 0:
            self.EventLoop.run_until_complete(asyncio.wait(taskList))

    def LoadAll(self, step=50, headers=None):
        continueable = True
        page = 1
        while continueable:
            for key in self.Flags:
                continueable = continueable and (page >= self.Flags[key])
            continueable = not continueable
            self.Loads(basePage=page, topPage=page+step, headers=headers)
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

    async def LoadPage(self, target: dict, page: int, keyWord: str, headers: dict):
        response = {}
        try:
            url = target.get('url') % (page)
        except:
            raise KeyError
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as res:
                # 请求成功则拉取Json报文。
                if res.status == 200:
                    response = json.loads(await res.text())
                else:
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
