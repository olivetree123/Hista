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
        bucket_id = request.args.get("bucket_id")
        if not (bucket_id and bucket_id.isdigit()):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.get_or_none(Bucket.id == int(bucket_id))
        b = b.to_json() if b else None
        return APIResponse(data=b)
    
    def post(self):
        """
        创建 bucket
        """
        name = request.get_json().get("name")
        public = request.get_json().get("public", 0)
        if not (name and public in [0, 1]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.add(name=name, public=public)
        r = b.to_json() if b else None
        return APIResponse(data=r)

    def put(self):
        """
        更新 bucket
        """
        bucket_id = request.get_json().get("bucket_id")
        name = request.get_json().get("name")
        public = request.get_json().get("public", 0)
        if not (bucket_id and isinstance(bucket_id, int) and public in [0, 1]):
            return APIResponse(code=BAD_REQUEST)
        b = Bucket.renew(bucket_id, name=name, public=public)
        r = b.to_json() if b else None
        return APIResponse(data=r)
        