import asyncio
import time

async def main(i):
    for l in range(10):
        print("%d-%d"%(i,l))
        await asyncio.sleep(i)

loop = asyncio.get_event_loop()
tasks = [loop.create_task(main(i)) for i in range(3)]
loop.run_until_complete(asyncio.wait(tasks))
