import asyncio
import aiohttp
import json


class Navigator:
    def __init__(self, searchMsg):
        """构造函数
        接收一个代表检索方式信息的字典作为参数，并建立空对象。

        Args:
            searchMsg: 描述检索方式的信息，应为一个字典，可通过json报文转化所得，并满足以下结构：
                {
                    "keyword": "正在抽奖",               //检索关键词，通常为正在抽奖。
                    "targets": [                        //检索目标的地址列表，一般为bilibili各直播大区。
                        {
                            "name": "...",
                            "url: "https://.../..."
                        },
                        {
                            "name": "...",
                            "url: "https://.../.../..."
                        }
                        // ...
                    ]
                }

        Raises:
            并不会检索searchMsg的格式并抛出异常。
        """
        self.LiveRoomList = []
        self.SearchMsg = searchMsg

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
                        # 请求成功则异步拉取json报文。
                        if res.status == 200:
                            response = json.loads(await res.text())
                        else:
                            continue
                roomList = response.get('data').get('list')
                # 如果显示正在抽奖的关键字，则根据直播间ID生成链接。
                for roomData in roomList:
                    try:
                        if roomData.get('pendant_info').get('2').get('content') == keyWord:
                            self.LiveRoomList.append({
                                'roomid': roomData.get('roomid'),
                                'urid': roomData.get('uid'),
                                'parent_id': roomData.get('parent_id'),
                                'area_id': roomData.get('area_id'),
                                'url': "https://live.bilibili.com/"+roomData.get('roomid')
                            })
                            self.Count += 1
                            if self.Count-baseCount > count:
                                return
                        else:
                            continue
                    except:
                        continue
