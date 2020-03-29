import asyncio
import json

import aiofiles
import aiohttp

import Base


async def getSearchMsg(path: str) -> dict:
    async with aiofiles.open(path, encoding='utf-8') as file:
        contents = await file.read()
    return json.loads(contents)


async def main():
    navi = Base.Navigator(await getSearchMsg('SearchMsg.json'))
    await navi.Loads(topPage=5)
    print(len(navi.LiveRoomList))
    for i in navi.LiveRoomList:
        print(i)

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
