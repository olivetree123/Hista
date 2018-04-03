#coding:utf-8

from flask import request
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.bucket import Bucket
from utils.functions import file_md5
from utils.response import BAD_REQUEST
from base import resource_fields, APIResponse

class ObjListEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取 obj 列表
        """
        objs = Obj.list()
        objs = [obj.to_json() for obj in objs]
        return APIResponse(data=objs)