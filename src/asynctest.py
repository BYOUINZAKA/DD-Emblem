import asyncio
import time
import json
import re

def getMsgFromJsonFile(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        contents = file.read()
    return json.loads(contents)

cookie = getMsgFromJsonFile('E:\Python Tools\data\Headers.json').get('Cookie')
pattern = re.compile(r'bili_jct=(\w*);')
print(pattern.findall(cookie)[0])
