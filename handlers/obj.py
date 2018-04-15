#coding:utf-8
import os
from flask import request
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.host import Host
from models.bucket import Bucket
from utils.functions import file_md5
from utils.cache import set_cache, get_cache
from utils.response import BAD_REQUEST, BUCKET_NOT_FOUND
from base import resource_fields, APIResponse
from config import SERIAL_NUMBER_CACHE
from storage.hista import hista_save

class ObjEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 obj
        """
        name = request.args.get("name")
        bucket = request.args.get("bucket")
        if not (name and bucket):
            return APIResponse(code=BAD_REQUEST)
        r = Obj.get_by_name(bucket, name)
        r = r.to_json() if r else None
        return APIResponse(data=r)
    
    def post(self):
        """
        创建/更新 obj
        """
        name = request.get_json.get("name")
        info = request.get_json.get("info")
        md5  = request.get_json.get("md5")
        bucket = request.get_json.get("bucket")
        number = request.get_json.get("number", 1)
        finish = request.get_json.get("finish", 0)
        filename = request.get_json.get("filename")
        file_content = request.get_json.get("file_content")
        # f = request.files["file"]
        if not (name and bucket and f):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.get_by_name(bucket)
        if not b:
            return APIResponse(code=BUCKET_NOT_FOUND)
        host = Host.get_host_by_md5(md5)
        if finish == 1:
            obj = Obj.create_or_update(name=name, bucket=bucket, filename=filename, md5_hash=md5, host_id=host.id, info=info)
            obj = obj.to_json() if obj else obj
        else
            obj = None
        serial = get_cache(SERIAL_CACHE.format(md5))
        if number <= serial:
            return APIResponse(data=obj)
        hista_save(b.path, file_content, md5)
        set_cache(SERIAL_CACHE.format(md5), number)
        return APIResponse(data=obj)
    
    def delete(self):
        """
        删除 obj
        """
        name = request.get_json().get("name")
        bucket = request.get_json().get("bucket")
        if not (name and bucket):
            return APIResponse(code=BAD_REQUEST)
        obj = Obj.remove(bucket, name)
        return APIResponse()
        
