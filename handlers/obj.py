#coding:utf-8
import os
from flask import request
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.bucket import Bucket
from utils.functions import file_md5
from utils.response import BAD_REQUEST, BUCKET_NOT_FOUND
from base import resource_fields, APIResponse

class ObjEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 obj
        """
        obj_id = request.args.get("obj_id")
        action = request.args.get("action")
        if not (obj_id and obj_id.isdigit()):
            return APIResponse(code=BAD_REQUEST)
        r = Obj.get_or_none(Obj.id == int(obj_id))
        r = r.to_json() if r else None
        return APIResponse(data=r)
    
    def post(self):
        """
        创建/更新 obj
        """
        name = request.form.get("name")
        info = request.form.get("info")
        bucket_name = request.form.get("bucket_name")
        f = request.files["file"]
        if not (name and bucket_name and f):
            return APIResponse(code=BAD_REQUEST)
        md5_hash = file_md5(f)
        b = Bucket.get_by_name(bucket_name)
        if not b:
            return APIResponse(code=BUCKET_NOT_FOUND)
        if not os.path.exists(b.path):
            os.makedirs(b.path)
        f.seek(0)
        f.save(os.path.join(b.path, md5_hash))
        obj = Obj.create_or_update(name=name, bucket_name=bucket_name, filename=f.filename, md5_hash=md5_hash, info=info)
        obj = obj.to_json() if obj else obj
        return APIResponse(data=obj)
    
    def delete(self):
        """
        删除 obj
        """
        obj_id = request.get_json().get("obj_id")
        obj = Obj.remove(obj_id)
        return APIResponse()
        
