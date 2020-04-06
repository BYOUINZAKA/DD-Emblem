# 示例代码
import json
import os
import time

from fake_useragent import UserAgent

import ddemblem
from ddemblem import Proxy, Receiver, Roster

if __name__ == '__main__':
    print('开始读取...')
    # 读取文件里的cookies字符串构建headers，这里用了fake_useragent来生成随机头。
    # 在cookies.txt下提前放入cookie。
    with open("E:\Python Tools\data\cookies.txt", encoding='utf-8') as cookie:
        headers = ddemblem.CreateHeaders(UserAgent().firefox, cookie.read())

    start = time.time()
    # 构造Roster对象需要传入一个字典作为搜索信息。
    roster = Roster(ddemblem.GetSearchMsg())

    roster.LoadAll(step=80)             # 加载全部抽奖名单，step参数可以在直播高峰期适当调高。
    print("读取完毕，开始领奖。")

    # roster.Loads(basePage, topPage)   # 或是指定加载
    # 查看可领取列表。
    # for i in roster.LiveRoomList:
    #     print(i)
    # print(roster.Flags)

    receiver = Receiver(headers)        # 将请求头送入Receiver类。
    receiver.Start(roster)              # 将名单送入Receiver类并启动。
    end = time.time()

    print("可领取直播间数量为%d个。\n共领取%d点亲密度。\n总计用时%ds。" %
          (len(roster.LiveRoomList), receiver.Score, end-start))

    os.system('pause')
