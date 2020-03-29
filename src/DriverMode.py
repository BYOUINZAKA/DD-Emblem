import asyncio

import selenium

from Base import Navigator


class Catcher():
    def __init__(self):
        super().__init__()

    async def Start(self, navigator: Navigator):
        return 0

    async def Dispose(self, liverMsg) -> bool:
        return 0
