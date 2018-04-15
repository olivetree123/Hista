#coding:utf-8

from flask_restful import Api

from config import ROLE
from handlers.bucket import BucketEndpoint
from handlers.bucket_list import BucketListEndpoint
from handlers.obj import ObjEndpoint
from handlers.obj_list import ObjListEndpoint
from handlers.obj_download import ObjDownloadEndpoint
from handlers.file import FileEndpoint

api = Api()

if ROLE == "master":
    api.add_resource(BucketEndpoint,     "/api/bucket",      endpoint="bucket")
    api.add_resource(BucketListEndpoint, "/api/bucket/list", endpoint="bucket_list")
    api.add_resource(ObjEndpoint,     "/api/object",      endpoint="object")
    api.add_resource(ObjListEndpoint, "/api/object/list", endpoint="object_list")
    api.add_resource(ObjDownloadEndpoint, "/api/object/download", endpoint="object_download")

elif ROLE == "slave":
    # slave 需要实现存储数据的接口
    api.add_resource(FileEndpoint, "/api/file", endpoint="file")

else:
    raise Exception("INVALID ROLE = {}. Role should be master or slave.".format(ROLE))