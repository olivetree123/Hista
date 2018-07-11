#coding:utf-8

from flask_restful import Api

from config import ROLE
from models.init import init_db
from handlers.file import FileEndpoint
from handlers.host import HostEndpoint
from handlers.bucket import BucketEndpoint, BucketListEndpoint
from handlers.obj import ObjEndpoint, ObjListEndpoint, ObjDownloadEndpoint

api = Api()

api.add_resource(FileEndpoint, "/api/file", endpoint="file")

if ROLE.upper() == "MASTER":
    init_db()
    api.add_resource(HostEndpoint,     "/api/host",      endpoint="host")
    api.add_resource(BucketEndpoint,     "/api/bucket",      endpoint="bucket")
    api.add_resource(BucketListEndpoint, "/api/bucket/list", endpoint="bucket_list")
    api.add_resource(ObjEndpoint,     "/api/object",      endpoint="object")
    api.add_resource(ObjListEndpoint, "/api/object/list", endpoint="object_list")
    api.add_resource(ObjDownloadEndpoint, "/api/object/download", endpoint="object_download")

elif ROLE.upper() == "SLAVE":
    # slave 需要实现存储数据的接口
    pass

else:
    raise Exception("INVALID ROLE = {}. Role should be master or slave.".format(ROLE))
