import asyncio
import json
import random
import time

# import aiofiles
# 已弃用
import aiohttp

from Base import Navigator
from HttpEngine import Catcher


def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


async def func(liver):
    return await Catcher.Dispose(liver, headers={})


if __name__ == '__main__':
    '''
    headers = getMsgFromJsonFile('Headers.json')
    print(headers)
    '''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    navi = Navigator(getMsgFromJsonFile('SearchMsg.json'))
    start = time.time()
    navi.Loads(topPage=(int(input("输入最大页数："))))
    end = time.time()
    for i in navi.LiveRoomList:
        print(i)
    print("可抽奖直播间数量为：%d" % len(navi.LiveRoomList))
    print("用时%ds" % (end-start))

    task = navi.EventLoop.create_task(func(random.choice(navi.LiveRoomList)))
    navi.EventLoop.run_until_complete(task)
