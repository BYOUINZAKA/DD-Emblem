import asyncio
import json

import aiohttp

from Base import Navigator


class Catcher():
    """ 进行抽奖操作的接口类
    通过HTTP请求进行批量的抽奖操作，速度较快，对于内存的占用较低。
    HttpEngine.Catcher的所有接口都与DriverEngine.Catcher的接口完全一致，可以相互替代。

    """
    async def Start(self, navigator: Navigator):
        return 0

    async def Dispose(liverMsg, headers):
        """ HTTP请求方式的亲密度领取函数
        按照b站的API来看，需要先请求一次权限，第二次请求才能得到舰队抽奖的id，接着再通过id来发出post请求。

        """
        senderList = []
        roomid = liverMsg.get('roomid')
        # id=2269734&roomid=21725051&type=guard&csrf_token=0a9411b47ea484e4a0b26a27a20082d0&csrf=0a9411b47ea484e4a0b26a27a20082d0&visit_id=
        async with aiohttp.ClientSession() as session:
            try:
                enableURL = "https://api.live.bilibili.com/av/v1/SuperChat/enable?room_id=%s&parent_area_id=%s&area_id=%s&ruid=%s" % (
                    roomid, liverMsg.get('parent_id'), liverMsg.get('area_id'), liverMsg.get('ruid'))
            except:
                raise KeyError
            async with session.get(enableURL) as enableRes:
                if enableRes.status == 200:
                    # print(await enableRes.text())
                    async with session.get("https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/Check?roomid=%s" % (roomid)) as checkRes:
                        senderList = (json.loads(await checkRes.text())).get('data').get('guard')
                        print(senderList)
                        print(len(senderList))
                else:
                    return -1
            '''
            for msg in senderList:
                data = {
                    'id': msg.get('id'),
                    'roomid': roomid,
                    'type': 'guard',
                    'csrf_token': '0a9411b47ea484e4a0b26a27a20082d0',
                    'csrf': '0a9411b47ea484e4a0b26a27a20082d0',
                    'visit_id': ''
                }
                url = "https://api.live.bilibili.com/xlive/lottery-interface/v3/guard/join"
                async with session.post(url, data=data, headers=headers) as response:
                    print(await response.text())
            '''
