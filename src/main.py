import aiohttp
import asyncio
import json
import Base


async def main():
    # url = 'https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=5&cate_id=0&area_id=0&sort_type=sort_type_8&page=1&page_size=30&tag_version=1'
    url = "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=sort_type_121&page=1&page_size=30&tag_version=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print(res.status)
            response = json.loads(await res.text())
            # print(json.loads(await res.text()))
    roomList = response.get('data').get('list')
    for roomData in roomList:
        # print(roomData['roomid'])
        try:
            if roomData.get('pendant_info').get('2').get('content') == "正在抽奖":
                d = {
                    'roomid': roomData.get('roomid'),
                    'urid': roomData.get('uid'),
                    'parent_id': roomData.get('parent_id'),
                    'area_id': roomData.get('area_id'),
                    'url': "https://live.bilibili.com/"+roomData.get('roomid')
                }
                print(roomData.get('roomid'))
            else:
                continue
        except:
            continue

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
