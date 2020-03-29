import asyncio
import json

# import aiofiles
# 已弃用
import aiohttp

from Base import Navigator


def getSearchMsg(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


if __name__ == '__main__':
    navi = Navigator(getSearchMsg('SearchMsg.json'))
    navi.Loads(topPage=(int(input("输入最大页数："))))
    print("可抽奖直播间数量为：%d" % len(navi.LiveRoomList))
    for i in navi.LiveRoomList:
        print(i)
