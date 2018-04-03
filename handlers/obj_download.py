#coding:utf-8

import os
import mimetypes
from flask import request
from flask import make_response
from flask_restful import Resource, marshal_with

from models.obj import Obj
from models.bucket import Bucket
from utils.functions import file_md5
from utils.response import BAD_REQUEST
from base import resource_fields, APIResponse

class ObjDownloadEndpoint(Resource):

    def get(self):
        """
        获取 obj 列表
        """
        obj_id = request.args.get("obj_id")
        action = request.args.get("action")
        if not (obj_id and obj_id.isdigit()):
            return APIResponse(code=BAD_REQUEST)
        r = Obj.get_or_none(Obj.id == int(obj_id))
        if not r:
            return APIResponse(data=r)
        b = Bucket.get_by_name(r.bucket_name)
        content = ""
        with open(os.path.join(b.path, r.md5_hash), "rb") as f:
            content = f.read()
        response = make_response(content)
        mime_type = mimetypes.guess_type(r.filename)[0]
        response.headers['Content-Type'] = mime_type
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(r.filename.encode().decode('latin-1'))
        return response