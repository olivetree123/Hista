#coding:utf-8

import os
from flask import request
from flask_restful import Resource, marshal_with

from models.host import Host
from base import resource_fields, APIResponse

class HostEndpoint(Resource):

    decorators = [marshal_with(resource_fields)]

    def get(self):
        """
        获取主机信息
        """
        host_id = request.args.get("host_id")
        host = Host.get_or_none(Host.id == host_id)
        host = host.to_json() if host else None
        return APIResponse(code=0, data=host)

    def post(self):
        """
        添加主机
        """
        name = request.get_json().get("name")
        path = request.get_json().get("path")
        ip_addr = request.get_json().get("ip_addr")
        username = request.get_json().get("username")
        password = request.get_json().get("password")
        host = Host.create_host(name, path, ip_addr, username, password)
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