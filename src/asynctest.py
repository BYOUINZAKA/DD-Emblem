import asyncio
import time
import HttpEngine


async def main():
    msg = {
        'roomid': '1420300',
        'parent_id': '5',
        'area_id': '192',
        'ruid': '45280964'
    }
    ca = HttpEngine.Catcher()
    await ca.Dispose(msg)

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
