import asyncio

import aiohttp

from Base import Navigator


class Catcher():
    """ 进行抽奖操作的接口类
    通过HTTP请求进行批量的抽奖操作，速度较快，对于内存的占用较低。
    HttpEngine.Catcher的所有接口都与DriverEngine.Catcher的接口完全一致，可以相互替代。

    """

    async def Start(self, navigator: Navigator):
        return 0

    async def Dispose(self, liverMsg: dict) -> int:
        """ HTTP请求方式的亲密度领取函数
        按照b站的API来看，需要先请求一次权限，第二次请求才能得到舰队抽奖的id，接着再通过id来发出post请求。

        """
        
