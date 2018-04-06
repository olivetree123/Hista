#coding:utf-8

from flask import request
from flask_restful import Resource, marshal_with

from base import resource_fields, APIResponse
from models.bucket import Bucket

class BucketListEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 bucket 列表
        """
        bks = Bucket.list_bucket()
        bks = [b.to_json() for b in bks]
        return APIResponse(data=bks)