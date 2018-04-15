#coding:utf-8
import os
from flask import request
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.bucket import Bucket
from utils.functions import file_md5
from utils.cache import set_cache, get_cache
from utils.response import BAD_REQUEST, BUCKET_NOT_FOUND
from base import resource_fields, APIResponse
from config import SERIAL_NUMBER_CACHE
from storage.hista import save

class FileEndpoint(Resource):

    def get(self):
        name = request.args.get("name")
        bucket = request.args.get("bucket")
        if not (name and bucket):
            return ""
        obj = Obj.get_by_name(bucket, name)
        bucket = Bucket.get_by_name(bucket)
        file_path = os.path.join(bucket.path, obj.md5_hash)
        if not os.path.exists(file_path):
            return ""
        content = ""
        with open(file_path, "rb") as f:
            content = f.read()
        response = make_response(content)
        mime_type = mimetypes.guess_type(obj.filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(obj.filename.encode().decode('latin-1'))
        return response

    @marshal_with(resource_fields)
    def post(self):
        # 存储文件
        md5  = request.get_json.get("md5")
        path = request.get_json.get("path")
        content = request.get_json.get("content")
        save(path, content, md5)
        return APIResponse()
    