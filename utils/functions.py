#coding:utf-8

import peewee
import hashlib
from datetime import datetime
from base64 import b64encode, b64decode

from config import UTC_DATETIME_FORMAT

def file_md5(f):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def datetime_to_str(_datetime, _format=UTC_DATETIME_FORMAT):
    return _datetime.strftime(_format)

def field_to_json(value):
    ret = value
    if isinstance(value, datetime):
        ret = datetime_to_str(value)
    elif isinstance(value, list):
        ret = [field_to_json(_) for _ in value]
    elif isinstance(value, dict):
        ret = {k: field_to_json(v) for k, v in value.items()}
    elif isinstance(value, bytes):
        ret = value.decode("utf-8")
    elif isinstance(value, bool):
        ret = int(ret)
    return ret

def str_to_int(value):
    if isinstance(value, int):
        return value
    if isinstance(value, (bytes, str)):
        assert value.isdigit()
        return int(value)
    raise Exception("Can not convert {} to int".format(value))