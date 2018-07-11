#coding:utf-8

"""
部署 server
"""

from flask_script import Command, Option

from utils.hista import create_host_by_host

class AddServer(Command):
    """
    部署 hista
    """

    option_list = (
        Option("--bootstrap-server", dest="server_list", default="localhost")
    )

    def run(self, server_list):
        server_list = server_list.split(",")
        if not server_list:
            return False
        map(create_host_by_host, server_list)
        print("Success to add servers, server_list = {}".format(server_list))
        return True