import asyncio

import selenium

from Base import Navigator


class Reciver():
    """ 进行抽奖操作的接口类
    基于webdriver的方式来完成抽奖操作，未实现。
    """
    def __init__(self):
        super().__init__()

    def Start(self, navigator: Navigator):
        return 0

    async def Get(self, liverMsg):
        return 0
