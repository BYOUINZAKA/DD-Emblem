import asyncio
import json
import re

import aiohttp
import async_timeout

from Base import Navigator
from Helper import HttpHelper


class Catcher():
    """ 进行抽奖操作的接口类
    通过HTTP请求方式来完成抽奖操作，速度较快，占用内存较少。
    但比较容易失败，并需要录入cookie数据。
    HttpEngine.Catcher的所有接口都与DriverEngine.Catcher的接口完全一致，可以相互替代。

    """

    def __init__(self, headers: dict):
        self.EnableURL = "https://api.live.bilibili.com/av/v1/SuperChat/enable?room_id=%s&parent_area_id=%s&area_id=%s&ruid=%s"
        self.PostURL = "https://api.live.bilibili.com/xlive/lottery-interface/v3/guard/join"
        self.CheckURL = "https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/Check?roomid=%s"
        self.Record = {'score': 0, 'values': []}
        self.Headers = headers
        try:
            # 从cookie中筛选获取csrf_token，用于post操作。
            pattern = re.compile(r'bili_jct=(\w*);')
            self.CsrfToken = pattern.findall(self.Headers.get('Cookie'))[0]
        except:
            raise KeyError

    def Start(self, navigator: Navigator, timeout=1):
        """ 启动函数
        接口接受一个Base.Navigator作为参数，并依附于其事件循环，创建任务并管理日志输出。
        因为B站有舰长抽奖的直播间不会太多，直播高峰期也不过近百，所以这里为每个直播间都申请一个任务。
        """
        taskList = []
        for liverMsg in navigator.LiveRoomList:
            taskList.append(navigator.EventLoop.create_task(
                self.Receive(liverMsg, timeout)))
        navigator.EventLoop.run_until_complete(asyncio.wait(taskList))

    async def Receive(self, liverMsg: dict, timeout):
        """ 异步HTTP请求亲密度领取接口
        按照b站的API来看，需要先请求一次权限，第二次请求才能得到舰队抽奖的id，接着再通过id来发出post请求
        post请求设有csrf防御，需要解析cookie。

        Args:
            liverMsg: 直播间数据的字典，结构形如Base.Navigator.LiveRoomList的元素。
            headers: HTTP请求头，用于post请求，需要包含cookie信息。

        Returns:
            返回值为一个字典，用于记录领取的日志或是错误日志，结构为。
            {
                'score': int,   # 领取的亲密度的结果总和，如果因为请求失败而意外返回，值为-1。
                'values: [      # 记录每一次领取的结果序列，元素为字典结构。
                    {
                        'success': int, # 领取结果，-1为请求失败，其他结果为取得的亲密度值。
                        'message': str  # 回复信息，为一个字符串。
                    }
                    # ... ...
                ]
            }

        Raises:
            KeyError: 字典结构错误。

        """
        senderList = []
        roomid = ""
        self.Headers['Referer'] = liverMsg.get('url')
        async with aiohttp.ClientSession() as session:
            # 第一次请求，调用enable，取得权限。
            try:
                roomid = liverMsg.get('roomid')
                enableURL = self.EnableURL % (
                    roomid, liverMsg.get('parent_id'), liverMsg.get('area_id'), liverMsg.get('ruid'))
            except:
                raise KeyError
            async with session.get(enableURL) as enableRes:
                if enableRes.status == 200:
                    # 第二次请求，调用check，取得信息。
                    async with session.get(self.CheckURL % (roomid)) as checkRes:
                        # 从回复报文中抽取出上舰信息的列表，其中维护了post所需的id。
                        senderList = (json.loads(await checkRes.text())).get('data').get('guard')
                        # print(json.dumps(senderList, indent=2))
                else:
                    HttpHelper.addRecordMsg(
                        self.Record, roomid, "Bad get.", -1)
            for msg in senderList:
                # 生成请求数据
                data = {
                    'id': msg.get('id'),
                    'roomid': roomid,
                    'type': msg.get('keyword'),
                    'csrf_token': self.CsrfToken,
                    'csrf': self.CsrfToken,
                    'visit_id': ''
                }
                # 在请求头中修改传输长度。
                self.Headers['Content-Length'] = HttpHelper.getContentLength(
                    data)
                try:
                    with async_timeout.timeout(timeout):
                        async with session.post(self.PostURL, data=data, headers=self.Headers) as res:
                            if res.status == 200:
                                response = json.loads(await res.text())
                                print(response)
                                if response.get('code') == 0:  # code=0 时，代表领取成功
                                    HttpHelper.addRecordMsg(self.Record, roomid, "Succeed.", int(
                                        response.get('data').get('award_num')))
                                else:  # code=400 时，代表已领取
                                    HttpHelper.addRecordMsg(self.Record, roomid,
                                                            "Already received.", 0)
                            else:
                                HttpHelper.addRecordMsg(
                                    self.Record, roomid, "Bad post.", -1)
                                continue
                except asyncio.TimeoutError as e:
                    # senderList.append(msg)
                    HttpHelper.addRecordMsg(
                        self.Record, roomid, "Time out error.", -1)
                    continue
