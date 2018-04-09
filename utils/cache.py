#coding:utf-8

import json
import redis
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def set_cache(key, value, src_type=""):
    if src_type == "json":
        value = json.dumps(value)
    r.set(key, value)

def get_cache(key, target_type=""):
    value = r.get(key)
    if target_type == "int":
        if isinstance(value, int):
            return value
        if isinstance(value, (str, bytes)) and value.isdigit():
            return int(value)
        print("Can not convert to int, value = ", value)
        return 0
    elif target_type == "json":
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                print("Can not convert {} to json.".format(value))
            return None
        else:
            print("Can not convert type {} to json.".format(type(value)))
            return None
    return value