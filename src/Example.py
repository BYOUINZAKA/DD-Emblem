import asyncio
import json
import time

import aiohttp

from Base import Navigator
from HttpEngine import Receiver


def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


if __name__ == '__main__':
    # 读取headers，需要包含Cookie，Content-Length，Referer字段。
    headers = getMsgFromJsonFile('E:\Python Tools\data\Headers.json')
    navi = Navigator(getMsgFromJsonFile('SearchMsg.json'))

    # 输入页数，Windows下由于打开文件限度为509，平均下来为80页。
    # 但是由于某些分区的直播数较少，所以设为100也不会有问题。
    topPage = int(input("输入最大页数："))

    start = time.time()
    navi.Loads(topPage=topPage)     # 加载抽奖名单。
    receiver = Receiver(headers)    # 将请求头送入Receiver类。
    receiver.Start(navi)            # 将名单送入Receiver类，启动。
    end = time.time()

    # 查看可领取列表。
    for i in navi.LiveRoomList:
        print(i)
    print("可抽奖直播间数量为：%d" % len(navi.LiveRoomList))

    # 领取完毕后浏览日志，也可以同步输出日志。
    for i in receiver.Record.get('values'):
        print(i)

    print("用时：%ds，共领取：%d点亲密度。" % (end-start, receiver.Record.get('score')))
