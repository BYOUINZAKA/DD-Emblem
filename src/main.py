import aiohttp
import asyncio
import json
import Base


async def main():
    url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=5&cate_id=0&area_id=0&sort_type=sort_type_8&page=1&page_size=30&tag_version=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print(res.status)
            response = json.loads(await res.text())
            # print(json.loads(await res.text()))
    roomList = response.get('data').get('list')
    for roomData in roomList:
        try:
            if roomData.get('pendant_info').get('2').get('content') == '正在抽奖':
                print(roomData.get('roomid'))
                if self.Count-baseCount > count:
                    return
            else:
                continue
        except:
            continue

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
d = {
    '1': {
        '11': 'abc',
        '22': ''
    },
    '2': 'ab',
    '3': {
        '31': 'abc',
        '32': {
            '321': 'abcd'
        }
    }
}
for va in d:
    try:
        value = d[va]['11']
    except:
        continue
    print(value)
