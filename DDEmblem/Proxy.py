import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Proxy():
    def __init__(self):
        super().__init__()
        self.IPList = []
        self.ProtoIPList = []
        event = asyncio.get_event_loop()
        dowloadTasks = []
        for page in range(1, 5):
            dowloadTasks.append(event.create_task(self.Download(page)))
        event.run_until_complete(asyncio.wait(dowloadTasks))
        print(self.ProtoIPList)
        taskList = []
        for ip in self.ProtoIPList:
            taskList.append(event.create_task(Proxy.Check(ip)))
        event.run_until_complete(asyncio.wait(taskList))

    async def Download(self, page):
        headers = {'User-Agent': UserAgent().firefox}
        async with aiohttp.ClientSession() as session:
            async with session.get("http://www.66ip.cn/mo.php?sxb=&tqsl=300&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=" % page, headers=headers) as res:
                soup = BeautifulSoup(await res.text(), 'html.parser')
                ips = soup.find_all('tr')
                for i in range(1, len(ips)):
                    ip_info = ips[i]
                    tds = ip_info.find_all('td')
                    if tds[5].text == 'HTTP':
                        self.ProtoIPList.append("http://%s:%s" %
                                                (tds[1].text, tds[2].text))
                    else:
                        self.ProtoIPList.append("https://%s:%s" %
                                                (tds[1].text, tds[2].text))

    async def Check(ip):
        # conn=aiohttp.TCPConnector(verify_ssl=False)
        headers = {'User-Agent': UserAgent().firefox}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.live.bilibili.com/room/v1/Index/getHotList", headers=headers, proxy=ip, timeout=1) as res:
                    print("%s合格" % ip)
        except:
            return
