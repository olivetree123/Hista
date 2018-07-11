#coding:utf-8

import os
from flask import request
from flask_restful import Resource, marshal_with

from models.host import Host
from utils.response import BAD_REQUEST
from base import resource_fields, APIResponse

class HostEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self, uid):
        """
        获取主机信息
        """
        host = Host.get_by_uid(uid)
        host = host.to_json() if host else None
        return APIResponse(code=0, data=host)

    def post(self):
        """
        添加主机
        """
        params = request.get_json()
        if not params:
            return APIResponse(code=BAD_REQUEST)
        name = params.get("name")
        path = params.get("path")
        port = params.get("port")
        ip_addr = params.get("ip_addr")
        username = params.get("username")
        password = params.get("password")
        host = Host.create_host(name, path, ip_addr, port, username, password)
        host = host.to_json() if host else None
        return APIResponse(code=0, data=host)


class HostListEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取主机列表
        """
        host_list = Host.list()
        host_list = [host.to_json() for host in host_list]
        return APIResponse(code=0, data=host_list)
