import asyncio
import json
import re

import aiohttp
import async_timeout

from Base import Navigator


class Catcher():
    """ 进行抽奖操作的接口类
    通过HTTP请求方式来完成抽奖操作，速度较快，占用内存较少。
    但比较容易失败，并需要录入cookie数据。
    HttpEngine.Catcher的所有接口都与DriverEngine.Catcher的接口完全一致，可以相互替代。

    """
    def Start(navigator: Navigator, headers: str, record: str):
        """ 启动函数
        接口接受一个Base.Navigator作为参数，并依附于其事件循环，创建任务并管理日志输出。
        因为B站有舰长抽奖的直播间不会太多，直播高峰期也不过近百，所以这里为每个直播间都申请一个任务。
        """
        # 用正则表达式从cookie中筛选获取csrf_token
        pattern = re.compile(r'bili_jct=(\w*);')
        csrf = pattern.findall(headers.get('Cookie'))[0]
        return 0

    async def Get(liverMsg: dict, headers: str) -> dict:
        """ 异步HTTP请求方式的亲密度领取函数
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
        record = {'score': 0, 'values': []}
        roomid = ""
        headers['Referer'] = liverMsg.get('url')
        async with aiohttp.ClientSession() as session:
            # 第一次请求，调用enable，取得权限。
            try:
                roomid = liverMsg.get('roomid')
                enableURL = "https://api.live.bilibili.com/av/v1/SuperChat/enable?room_id=%s&parent_area_id=%s&area_id=%s&ruid=%s" % (
                    roomid, liverMsg.get('parent_id'), liverMsg.get('area_id'), liverMsg.get('ruid'))
            except:
                raise KeyError
            async with session.get(enableURL) as enableRes:
                if enableRes.status == 200:
                    # 第二次请求，调用check，取得信息。
                    async with session.get("https://api.live.bilibili.com/xlive/lottery-interface/v1/lottery/Check?roomid=%s" % (roomid)) as checkRes:
                        # 从回复报文中抽取出上舰信息的列表，其中维护了post所需的id。
                        senderList = (json.loads(await checkRes.text())).get('data').get('guard')
                        # print(json.dumps(senderList, indent=2))
                else:
                    return {
                        'score': -1,
                        'values': [{'success': -1, 'message': ("Get request failed. url='%s'" % (enableURL))}]
                    }
            # 用正则表达式从cookie中筛选获取csrf_token
            pattern = re.compile(r'bili_jct=(\w*);')
            csrf = pattern.findall(headers.get('Cookie'))[0]
            for msg in senderList:
                data = {
                    'id': msg.get('id'),
                    'roomid': roomid,
                    'type': msg.get('keyword'),
                    'csrf_token': csrf,
                    'csrf': csrf,
                    'visit_id': ''
                }
                url = "https://api.live.bilibili.com/xlive/lottery-interface/v3/guard/join"
                with async_timeout.timeout(1):
                    try:
                        async with session.post(url, data=data, headers=headers) as res:
                            if res.status == 200:
                                response = json.loads(await res.text())
                                print(response)
                                if response.get('code') == 0:
                                    award_num = int(
                                        response.get('data').get('award_num'))
                                    record['score'] += award_num
                                    record.get('values').append(
                                        {'success': award_num, 'message': ("Success. roomid=%s id=%s" % (roomid, msg.get('id')))})
                                else:
                                    record.get('values').append(
                                        {'success': 0, 'message': ("Already got. roomid=%s id=%s" % (roomid, msg.get('id')))})

                            else:
                                record.get('values').append(
                                    {'success': -1, 'message': ("Bad post. roomid=%s id=%s" % (roomid, msg.get('id')))})
                                continue
                    except Exception as e:
                        print(e)
                        record.get('values').append(
                            {'success': -1, 'message': ("Time out error. roomid=%s id=%s" % (roomid, msg.get('id')))})
                        continue
                        # senderList.append(msg)
        return record
