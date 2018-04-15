#coding:utf-8

from flask import request
from flask_restful import Resource, marshal_with

from base import resource_fields, APIResponse
from models.bucket import Bucket
from utils.response import BAD_REQUEST
from utils.functions import str_to_int

class BucketEndpoint(Resource):
    
    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 bucket 信息
        """
        name = request.args.get("name")
        if not name:
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.get_by_name(name)
        b = b.to_json() if b else None
        return APIResponse(data=b)
    
    def post(self):
        """
        创建 bucket
        """
        name = request.get_json().get("name")
        info = request.get_json().get("info")
        public = request.get_json().get("public", 0)
        if not (name and public in [0, 1]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.add(name=name, public=public, info=info)
        r = b.to_json() if b else None
        return APIResponse(data=r)

    def put(self):
        """
        更新 bucket
        """
        name = request.get_json().get("name")
        info = request.get_json().get("info")
        public = request.get_json().get("public", None)
        if not (name and public in [0, 1, None]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.renew(name=name, public=public, info=info)
        r = b.to_json() if b else None
        return APIResponse(data=r)
    
    def delete(self):
        """
        删除 bucket
        """
        name = request.get_json().get("name")
        if not name:
            return APIResponse(code=BAD_REQUEST)
        Bucket.remove(name)
        return APIResponse()


class BucketListEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 bucket 列表
        """
        bks = Bucket.list_bucket()
        bks = [b.to_json() for b in bks]
        return APIResponse(data=bks)