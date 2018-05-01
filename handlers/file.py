#coding:utf-8
import os
import mimetypes
from flask import request, make_response
from flask_restful import Resource, marshal_with

from config import DATA_PATH
from models.obj import Obj
from models.bucket import Bucket
from utils.functions import file_md5
from utils.cache import set_cache, get_cache
from utils.response import BAD_REQUEST, BUCKET_NOT_FOUND
from base import resource_fields, APIResponse
from storage.hista import local_save

class FileEndpoint(Resource):

    def get(self):
        md5 = request.args.get("md5")
        bucket = request.args.get("bucket")
        if not (md5 and bucket):
            return ""
        file_path = os.path.join(DATA_PATH, bucket, md5)
        if not (os.path.exists(file_path) and os.path):
            return ""
        with open(file_path, "rb") as f:
            content = f.read()
        response = make_response(content)
        response.headers["Content-Disposition"] = "attachment; filename={}".format(md5)
        return response

    @marshal_with(resource_fields)
    def post(self):
        # 存储文件
        md5  = request.form.get("md5")
        bucket_path = request.form.get("bucket_path")
        chunk_num  = int(request.form.get("chunk_num", 1))
        total_chunk  = int(request.form.get("total_chunk", 1))
        f = request.files["file"]
        local_save(chunk_num, bucket_path, f.read(), md5, total_chunk)
        return APIResponse()
    