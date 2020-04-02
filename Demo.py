# 示例代码
import json
import os
import time

from fake_useragent import UserAgent

from ddemblem import Base, Engine

if __name__ == '__main__':
    # 读取文件里的cookies字符串构建headers，这里用了fake_useragent来生成随机头。
    with open("E:\Python Tools\data\cookies.txt", encoding='utf-8') as cookie:
        headers = Base.createHeaders(UserAgent().firefox, cookie.read())

    start = time.time()
    # 构造Roster对象需要传入一个字典作为搜索信息，可以使用SearchMsg.json或是HttpHelper.getSearchMsg()
    roster = Base.Roster(Base.getSearchMsg())

    roster.LoadAll(step=80)             # 加载全部抽奖名单，step参数可以在直播高峰期适当调高。
    # roster.Loads(basePage, topPage)   # 或是指定加载
    receiver = Engine.Receiver(headers) # 将请求头送入Receiver类。
    receiver.Start(roster)              # 将名单送入Receiver类并启动。
    end = time.time()

    # 可领取列表。
    for i in roster.LiveRoomList:
        print(i)
    print(roster.Flags)

    # 领取日志。
    for i in receiver.Record['values']:
        print("RoomID: {0:<10} Result: {1:<10} Message: {2:<10}".format(
            i['roomid'], i['success'], i['message']))

    print("可领取直播间数量为%d个。\n共领取%d点亲密度。\n总计用时%ds。" %
          (len(roster.LiveRoomList), receiver.Record['score'], end-start))

    os.system('pause')
