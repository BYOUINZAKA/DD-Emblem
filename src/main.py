import asyncio
import json
import time

# import aiofiles
# 已弃用
import aiohttp

from Base import Navigator


def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


if __name__ == '__main__':
    headers = getMsgFromJsonFile('Headers.json')
    navi = Navigator(getMsgFromJsonFile('SearchMsg.json'))
    start = time.time()
    navi.Loads(topPage=(int(input("输入最大页数："))))
    end = time.time()
    for i in navi.LiveRoomList:
        print(i)
    print("可抽奖直播间数量为：%d" % len(navi.LiveRoomList))
    print("用时%ds" % (end-start))
