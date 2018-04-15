#coding:utf-8

from flask_restful import Api

from config import ROLE
from handlers.file import FileEndpoint
from handlers.bucket import BucketEndpoint, BucketListEndpoint
from handlers.obj import ObjEndpoint, ObjListEndpoint, ObjDownloadEndpoint

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
