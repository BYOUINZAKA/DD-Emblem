import asyncio
import json
import random
import time

# import aiofiles
# 已弃用
import aiohttp

from Base import Navigator
from HttpEngine import Reciver


def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


if __name__ == '__main__':
    headers = getMsgFromJsonFile('E:\Python Tools\data\Headers.json')
    navi = Navigator(getMsgFromJsonFile('SearchMsg.json'))
    topPage = int(input("输入最大页数："))
    start = time.time()
    navi.Loads(topPage=topPage)
    '''
    for i in navi.LiveRoomList:
        print(i)
    '''
    print("可抽奖直播间数量为：%d" % len(navi.LiveRoomList))

    reciver = Reciver(headers)
    reciver.Start(navi)
    end = time.time()
    for i in navi.LiveRoomList:
        print(i)
    for i in reciver.Record.get('values'):
        print(i)
    print("用时：%ds" % (end-start))
    print("共领取：%d" % (reciver.Record.get('score')))
