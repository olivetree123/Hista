#coding:utf-8
import copy
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
        data = request.get_json()
        tp = data.pop("type", None)
        name = data.pop("name", None)
        desc = data.pop("desc", None)
        public = data.pop("public", 0)
        extra_info = data
        if extra_info and not isinstance(extra_info, dict):
            return APIResponse(code=BAD_REQUEST)
        if not (name and public in [0, 1]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.add(name=name, public=public, type=tp, desc=desc, extra_info=extra_info)
        r = b.to_json() if b else None
        return APIResponse(data=r)

    def put(self):
        """
        更新 bucket
        """
        data = request.get_json()
        tp = data.pop("type", None)
        name = data.pop("name", None)
        desc = data.pop("desc", None)
        public = data.pop("public", 0)
        extra_info = data
        if not (name and public in [0, 1, None]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.renew(name=name, public=public, desc=desc, extra_info=extra_info)
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
        data = request.args.to_dict()
        type = data.pop("type", None)
        status = data.pop("status", True)
        bks = Bucket.filter_bucket(status=status, type=type, **data)
        bks = [b.to_json() for b in bks]
        return APIResponse(data=bks)