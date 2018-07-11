#coding:utf-8
import os
import json
import requests
import mimetypes
from flask import request, make_response
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.host import Host
from models.bucket import Bucket
from utils.functions import file_md5, content_md5
from utils.cache import set_cache, get_cache
from utils.response import BAD_REQUEST, BUCKET_NOT_FOUND, OBJECT_NOT_FOUND, OBJECT_SAVE_FAILED
from base import resource_fields, APIResponse
from storage.hista import hista_save
from config import SERIAL_CACHE, DATA_PATH

class ObjEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self, uid):
        """
        获取 obj
        """
        r = Obj.get_by_uid(uid)
        r = r.to_json() if r else None
        return APIResponse(data=r)
    
    def post(self):
        """
        创建/更新 obj
        """
        data = request.form.to_dict()
        name = data.pop("name", None)
        desc = data.pop("desc", None)
        md5  = data.pop("md5", None)
        bucket = data.pop("bucket", None)
        content = data.pop("content", None)
        chunk_num = int(data.pop("chunk_num", 1))
        total_chunk = int(data.pop("total_chunk", 1))
        file_objs = request.files.get("file_name")
        extra_info = data
        b = Bucket.get_by_name(bucket)
        if not b:
            return APIResponse(code=BUCKET_NOT_FOUND)
        file_objs = file_objs if isinstance(file_objs, (list, tuple)) else [file_objs]
        result = []
        for file_obj in file_objs:
            filename = file_obj.filename if file_obj else request.form.get("filename")
            if not (content or file_obj):
                return APIResponse(code=BAD_REQUEST)
            content = content if content else str(file_obj.read(), encoding="latin-1")
            if not md5:
                md5 = content_md5(content.encode("latin-1"))
            # 需要一个异步 worker 来处理 io.
            r = hista_save(chunk_num, b.path, content, md5, total_chunk)
            if not r:
                return APIResponse(code=OBJECT_SAVE_FAILED)
            if chunk_num == total_chunk:
                host = Host.get_host_by_md5(md5)
                obj = Obj.create_or_update(name=name or md5, bucket=bucket, filename=filename or name, md5_hash=md5, host_id=host.id, desc=desc, extra_info=extra_info)
                obj = obj.to_json() if obj else obj
                result.append(obj)
            else:
                obj = None
        return APIResponse(data=result)
    
    def delete(self, uid):
        """
        删除 obj
        """
        obj = Obj.remove(uid)
        return APIResponse()


class ObjListEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 obj 列表
        """
        args = request.args.to_dict()
        bucket = args.pop("bucket")
        extra_info = args
        objs = Obj.list_obj(bucket, **extra_info)
        objs = [obj.to_json() for obj in objs] if objs else None
        return APIResponse(data=objs)
    
    def delete(self):
        """
        批量删除 obj
        """
        bucket    = request.get_json().get("bucket")
        name_list = request.get_json().get("name_list")
        if not (bucket and name_list and isinstance(name_list, (tuple, list))):
            return APIResponse(code=BAD_REQUEST)
        Obj.remove_objs(bucket, name_list)
        return APIResponse()


class ObjDownloadEndpoint(Resource):

    def get(self):
        """
        获取 obj
        """
        name = request.args.get("name")
        bucket = request.args.get("bucket")
        if not (name and bucket):
            return APIResponse(code=BAD_REQUEST)
        obj = Obj.get_by_name(bucket, name)
        if not obj:
            return APIResponse(code=OBJECT_NOT_FOUND)
        host = Host.get_or_none(Host.id == obj.host_id)
        if host.ip_addr == "localhost":
            with open(os.path.join(DATA_PATH, bucket, obj.md5_hash), "rb") as f:
                content = f.read()
        else:
            url = "http://{}:8001/api/file?bucket={}&md5={}".format(host.ip_addr, bucket, obj.md5_hash)
            r = requests.get(url)
            content = r.content
        response = make_response(content)
        mime_type = mimetypes.guess_type(obj.filename)[0]
        response.headers["Content-Type"] = mime_type
        response.headers["Content-Disposition"] = "attachment; filename={}".format(obj.filename.encode().decode("latin-1"))
        return response
