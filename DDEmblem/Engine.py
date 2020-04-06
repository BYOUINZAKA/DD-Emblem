import asyncio
import json
import re
import sys

import aiohttp
import async_timeout

from ddemblem import Base
from ddemblem.Base import Roster


class Receiver():
    """ 进行抽奖操作的接口类
    基于HTTP请求方式来完成抽奖操作，速度较快，占用内存较少。
    但有时会失败，并需要录入cookie数据。

    Members:
        Record: 记录日志字典，结构为：
            {
                'score': int,   # 领取的亲密度的总和。
                'values: [      # 记录每一次领取的结果序列，元素为字典结构。
                    {
                        'success': int, # 领取结果，-1为请求失败，其他结果为取得的亲密度值。
                        'message': str  # 回复信息，为一个字符串。
                    }
                    # ... ...
                ]
            }
        Headers:    HTTP请求头，需要包含Cookie，Content-Length，Referer字段。
        CsrfToken:  B站设有csrf防御，此字段为从cookie中读取的csrf_token。
        EnableURL:  enbable接口的地址，为一个格式化字符串。
        CheckURL:   check接口的地址，为一个格式化字符串。
        PostURL:    join接口的地址，用于post领取请求。
    """

    def __init__(self, headers: dict):
        """ 构造器
        Args: 
            headers: HTTP请求头，用于post请求，需要包含cookie信息。

        """
        self.Score = 0
        self.Headers = headers
        self.EnableURL = "https://api.live.bilibili.com/av/v1/SuperChat/enable?room_id=%s&parent_area_id=%s&area_id=%s&ruid=%s"
        self.PostURL = "https://api.live.bilibili.com/xlive/lottery-interface/v3/guard/join"
        self.CheckURL = "https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/Check?roomid=%s"
        try:
            # 从cookie中筛选获取csrf_token，用于post操作。
            pattern = re.compile(r'bili_jct=(\w*);')
            self.CsrfToken = pattern.findall(self.Headers.get('Cookie'))[0]
        except:
            raise KeyError

    def Start(self, roster: Roster, timeout=1, merge=1, delay=0, proxy=None, log=sys.stdout):
        """ 统一启动接口
        接口接受一个加载完毕的Base.Roster对象作为参数，并依附于其的事件循环，创建任务并管理日志输出。
        因为B站有舰长抽奖的直播间不会太多，直播高峰期也不过近百，所以这里为每个直播间都申请一个任务。

        Args: 
            roster:     一个Base.Roster对象。
            timeout:    超时限制，超过此值会post失败并输出日志。
            merge:      任务的串行程度，数值越低并发的程度越低，效率越高，一般可以适当提高数字增加运行时间。
            delay:      请求间的延迟，和merge配合降低运行效率防止IP被ban。
            proxy:      使用代理，默认不使用。
            log:        日志输出目标，为文件对象，默认为sys.stdout。
        """
        taskList = []
        # '''
        i = 0
        while i < len(roster.LiveRoomList):
            taskList.append(roster.EventLoop.create_task(
                self.LinearReceive(roster.LiveRoomList, i, timeout, merge, delay, proxy, log)))
            i += merge
        '''
        for liverMsg in roster.LiveRoomList:
            taskList.append(roster.EventLoop.create_task(
                self.Receive(liverMsg, timeout, proxy=proxy, log=log)))
        '''
        roster.EventLoop.run_until_complete(asyncio.wait(taskList))

    async def Receive(self, liverMsg: dict, timeout, proxy, log):
        """ 异步亲密度领取接口
        此接口领取一个直播间的所有抽奖。
        按照b站的API来看，需要先请求一次权限，第二次请求才能得到抽奖信息的id，接着再通过id来发出post请求
        post请求设有csrf防御，需要用到csrf_token。

        Args:
            liverMsg: 直播间数据的字典，结构形如Base.Roster.LiveRoomList的元素。

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
                    Base.log(
                        log, self.self.Score, roomid, "Bad get.", -1)
                    return
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
                self.Headers['Content-Length'] = Base.getContentLength(
                    data)
                try:
                    with async_timeout.timeout(timeout):
                        async with session.post(self.PostURL, data=data, headers=self.Headers) as res:
                            if res.status == 200:
                                await asyncio.sleep(0.1)
                                response = json.loads(await res.text())
                                # code=0 时，代表领取成功
                                if response.get('code') == 0:
                                    score = int(response.get(
                                        'data').get('award_num'))
                                    self.Score += score
                                    Base.log(log, self.Score, roomid,
                                             "Successful received.", score)
                                # code=400 时，代表已领取
                                elif response.get('code') == 400:
                                    Base.log(log, self.Score, roomid,
                                             "You already received.", 0)
                                else:
                                    Base.log(log, self.Score, roomid,
                                             response.get('message'), -1)
                            else:
                                # 请求失败时把信息抛到序列尾择期执行。
                                Base.log(
                                    log, self.Score, roomid, "Bad post and try again.", -1)
                                senderList.append(msg)
                                continue
                except asyncio.TimeoutError as e:
                    Base.log(
                        log, self.Score, roomid, "Time out error.", -1)
                    continue

    async def LinearReceive(self, liveRoomList: list, base: int, timeout, merge, delay, proxy, log):
        top = base+merge
        if top >= len(liveRoomList):
            top = len(liveRoomList)
        for i in range(base, top-1):
            await self.Receive(liveRoomList[i], timeout, proxy, log)
            await asyncio.sleep(delay)
        await self.Receive(liveRoomList[top-1], timeout, proxy, log)
