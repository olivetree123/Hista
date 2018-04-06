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
        bucket = request.args.get("bucket")
        objs = Obj.list_obj(bucket)
        objs = [obj.to_json() for obj in objs] if objs else None
        return APIResponse(data=objs)
    
    def delete(self):
        """
        批量删除 obj
        """
        bucket   = request.get_json().get("bucket")
        name_list = request.get_json().get("name_list")
        if not (bucket and name_list and isinstance(name_list, (tuple, list))):
            return APIResponse(code=BAD_REQUEST)
        Obj.remove_objs(bucket, name_list)
        return APIResponse()