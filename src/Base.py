import asyncio
import aiohttp
import json


class Navigator:
    def __init__(self, searchMsg):
        self.LiveRooms = []
        self.Count = 0
        self.SearchMsg = searchMsg

    async def Loads(self, headers, basePage=1, topPage=3, count=-1):
        baseCount = self.Count
        keyWord = self.SearchMsg.get('keyword')
        targets = self.SearchMsg.get('targets')
        for area in targets:
            target = targets.get(area)
            for page in range(basePage, topPage+1):
                response = {}
                url = target % (page)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as res:
                        if res.status == 200:
                            response = json.loads(await res.text())
                        else:
                            continue
                roomList = response.get('data').get('list')
                for roomData in roomList:
                    try:
                        if roomData.get('pendant_info').get('2').get('content') == keyWord:
                            self.LiveRooms.append(roomData.get('roomid'))
                            self.Count += 1
                            if self.Count-baseCount > count:
                                return
                        else:
                            continue
                    except:
                        continue
