#coding:utf-8

import os
import requests
import mimetypes
from flask import request
from flask import make_response
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.host import Host
from models.bucket import Bucket
from utils.functions import file_md5
from utils.response import BAD_REQUEST, OBJECT_NOT_FOUND
from base import resource_fields, APIResponse

class ObjDownloadEndpoint(Resource):

    def get(self):
        """
        获取 obj 列表
        """
        name = request.args.get("name")
        bucket = request.args.get("bucket")
        if not (name and bucket):
            return APIResponse(code=BAD_REQUEST)
        obj = Obj.get_by_name(bucket, name)
        if not obj:
            return APIResponse(code=OBJECT_NOT_FOUND)
        b = Bucket.get_by_name(bucket)
        # content = ""
        # with open(os.path.join(b.path, obj.md5_hash), "rb") as f:
        #     content = f.read()
        host = Host.get_or_none(Host.id == obj.host_id)
        url = "http://" + host.ip_addr + "/api/file"
        r = request.get(url)
        response = make_response(r.content)
        mime_type = mimetypes.guess_type(obj.filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(obj.filename.encode().decode('latin-1'))
        return response