#coding:utf-8

from nameko.rpc import rpc

from utils.hista import get_hosts


class RpcService:
    name = "rcp_service"

    @rpc
    def sync_data(self, tb_name, uid, md5_hash):
        return "Hello, {}!".format(name)

