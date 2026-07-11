import json
from email.policy import default
from typing import Any

import redis.asyncio as redis
import os
from dotenv import load_dotenv
load_dotenv()
REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
REDIS_PORT=int(os.getenv("REDIS_PORT", 6379))
REDIS_DB=int(os.getenv("REDIS_DB", 0))

#创建redis的连接对象
redis_client=redis.Redis(
    host=REDIS_HOST,#redis服务主机地址
    port=REDIS_PORT,#redis服务端口号
    db=REDIS_DB,#redis数据库编号 0-15
    protocol=2,
    decode_responses=True #设置返回结果为字符串类型

)
#读取:字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

#读取字典
async def get_json_cache(key:str):
    try:
        data= await redis_client.get(key)
        if data:
            return json.loads(data) #序列化
        return None
    except Exception as e:
        print(f"获取JSON缓存失败：{e}")
        return None
#设置缓存
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            value=json.dumps(value,ensure_ascii=False)
        await redis_client.set(key, value, ex=expire)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
async def delete_cache(key: str):
    try:
        await redis_client.delete(key)
        return True
    except Exception as e:
        print(f"删除缓存失败：{e}")
        return False