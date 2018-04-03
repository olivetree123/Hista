#coding:utf-8

from flask_restful import Api

from handlers.bucket import BucketEndpoint
from handlers.bucket_list import BucketListEndpoint
from handlers.obj import ObjEndpoint
from handlers.obj_list import ObjListEndpoint
from handlers.obj_download import ObjDownloadEndpoint

api = Api()

api.add_resource(BucketEndpoint,     "/api/bucket",      endpoint="bucket")
api.add_resource(BucketListEndpoint, "/api/bucket_list", endpoint="bucket_list")

api.add_resource(ObjEndpoint,     "/api/object",      endpoint="object")
api.add_resource(ObjListEndpoint, "/api/object/list", endpoint="object_list")
api.add_resource(ObjDownloadEndpoint, "/api/object/download", endpoint="object_download")
