# 示例代码
import json
import os
import time

from ddemblem.Base import Roster
from ddemblem.Helper import HttpHelper
from ddemblem.HttpEngine import Receiver


def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)


if __name__ == '__main__':
    # 读取headers，需要包含Cookie，Content-Length，Referer字段。
    # 可以使用 HttpHelper.createHeaders()
    # headers = HttpHelper.createHeaders(UserAgent().firefox, "Your cookie")
    headers = getMsgFromJsonFile('E:\Python Tools\data\Headers.json')

    # 构造Roster对象需要传入一个字典作为搜索信息，可以使用SearchMsg.json或是HttpHelper.getSearchMsg()
    roster = Roster(HttpHelper.getSearchMsg())

    # 最大页数由select()决定，Windows下打开文件限度为509，Linux下为1000。
    # 所以理论上Linux下的页数可以达到160左右，而Windows只有80。
    # 但是由于某些分区的直播数较少，所以Windows下设在100左右也不会有问题。
    topPage = int(input("输入最大页数："))

    start = time.time()
    roster.Loads(topPage=topPage)       # 加载抽奖名单。
    receiver = Receiver(headers)        # 将请求头送入Receiver类。
    receiver.Start(roster)              # 将名单送入Receiver类并启动。
    end = time.time()

    # 可领取列表。
    for i in roster.LiveRoomList:
        print(i)

    # 领取日志。
    for i in receiver.Record.get('values'):
        print("RoomID: {0:<10} Result: {1:<10} Message: {2:<10}".format(
            i['roomid'], i['success'], i['message']))

    print("可领取直播间数量为%d个。\n共领取%d点亲密度。\n总计用时%ds。" %
          (len(roster.LiveRoomList), receiver.Record.get('score'), end-start))

    os.system('pause')
