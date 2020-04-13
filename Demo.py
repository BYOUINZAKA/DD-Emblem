# 示例代码
import json
import os
import time

import ddemblem
from ddemblem import Proxy, Receiver, Roster


def GetSettings():
    # 根据时间选择合适的步长，并发数和延迟。
    hour = time.localtime(time.time()).tm_hour
    if hour <= 23 and hour >= 20:
        return {'step': 70, 'group': 4, 'delay': 0.1}
    elif hour < 20 and hour >= 17:
        return {'step': 70, 'group': 5, 'delay': 0.1}
    elif hour < 17 and hour >= 12:
        return {'step': 50, 'group': 0, 'delay': 0}
    elif hour < 12 and hour >= 3:
        return {'step': 30, 'group': 0, 'delay': 0}
    else:
        return {'step': 50, 'group': 8, 'delay': 0.1}


if __name__ == '__main__':
    setting = GetSettings()
    step = setting["step"]
    group = setting["group"]
    delay = setting["delay"]

    print('开始读取...')

    # 读取文件里的cookies字符串构建headers，这里用了fake_useragent来生成随机头。
    # 在cookies.txt下提前放入cookie。
    with open("E:\Python Tools\data\cookies.txt", encoding='utf-8') as cookie:
        headers = ddemblem.CreateHeaders(cookie.read())

    start = time.time()
    # 构造Roster对象需要传入一个字典作为搜索信息。
    roster = Roster(ddemblem.GetSearchMsg())

    try:
        roster.LoadAll(step=step)     # 加载全部抽奖名单，step参数可以在直播高峰期适当调高。
        # roster.Loads(10)
        print(roster.Flags)
    except:
        print("读取时产生错误。")

    print("读取完毕，开始领奖。")
    if len(roster.LiveRoomList) > 0:

        receiver = Receiver(headers)        # 将请求头送入Receiver类。
        # receiver.Start(roster)            # 将名单送入Receiver类直接启动。
        if group == 0:
            marge = 1
        else:
            marge = int(len(roster.LiveRoomList)/group)
        receiver.Start(roster=roster,       # 防ban启动，保证并发数最大为4，并附有0.1s的延迟来启动。
                       merge=marge,
                       delay=delay)
        end = time.time()

        print("可领取直播间数量为%d个。\n共领取%d点亲密度。\n总计用时%ds。" %
              (len(roster.LiveRoomList), receiver.Score, end-start))
    # os.system('pause')
