import asyncio
import json

import aiohttp


class Navigator:
    """ 可抽奖直播间的信息读取和储存的类

    Members: 
        LiveRoomList: 储存抽奖直播间信息的列表，元素皆为一个字典，结构为：
            {
                'roomid': '...',            # 直播间id。
                'urid': '...',              # 我也不知道这是什么，似乎是up主的id。
                'parent_id': '...'          # 大区所在id。
                'area_id': '...'            # 小分区id。
                'url': "https://xxx/..."    # 直播间链接。
            }
        SearchMsg: 检索方式信息。 

    Future: 1、区分一个直播间的奖品是否已被成功领取。
            2、识别直播间中抽奖信息的数量和类型。
    """

    def __init__(self, searchMsg):
        """ 构造器
        接收一个代表检索方式信息的字典作为参数，并建立空对象。

        Args:
            searchMsg: 描述检索方式的信息，应为一个字典，可通过json报文转化所得，并满足以下结构：
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

        Attention: 并不会对searchMsg的格式进行检索并抛出异常。
        """
        self.LiveRoomList = []
        self.SearchMsg = searchMsg

    def Push(self, roomId: str, urId: str, parentId: str, areaId: str, url: str):
        dic = {
            'roomid': roomId,
            'urid': urId,
            'parent_id': parentId,
            'area_id': areaId,
            'url': url
        }
        self.LiveRoomList.append(dic)
        return dic

    async def Loads(self, headers, basePage=1, topPage=3, count=-1):
        baseCount = len(self.LiveRoomList)
        keyWord = self.SearchMsg.get('keyword')
        targets = self.SearchMsg.get('targets')
        for area in targets:
            target = targets.get(area).get('url')
            for page in range(basePage, topPage+1):
                response = {}
                url = target % (page)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as res:
                        # 请求成功则异步拉取Json报文。
                        if res.status == 200:
                            response = json.loads(await res.text())
                        else:
                            continue
                roomList = response.get('data').get('list')
                # 如果显示正在抽奖的关键字，则读取直播间信息，并根据直播间ID生成链接。
                for roomData in roomList:
                    try:
                        if roomData.get('pendant_info').get('2').get('content') == keyWord:
                            self.LiveRoomList.append({
                                'roomid': roomData.get('roomid'),
                                'urid': roomData.get('uid'),
                                'parent_id': roomData.get('parent_id'),
                                'area_id': roomData.get('area_id'),
                                'url': "https://live.bilibili.com/%s" % (roomData.get('roomid'))
                            })
                            if len(self.LiveRoomList)-baseCount > count:
                                return
                        else:
                            continue
                    except:
                        continue
