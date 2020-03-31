import asyncio
import time
import json
import re
from Helper import HttpHelper

def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)

cookie = getMsgFromJsonFile('E:\Python Tools\data\Headers.json').get('Cookie')
pattern = re.compile(r'bili_jct=(\w*);')
print(pattern.findall(cookie)[0])
print(len("id=2276212&roomid=21710120&type=guard&csrf_token=0a9411b47ea484e4a0b26a27a20082d0&csrf=0a9411b47ea484e4a0b26a27a20082d0&visit_id="))
print(HttpHelper.getContentLength({}))