#coding:utf-8
from config import DATA_PATH, PORT
from models.host import Host

def create_host_by_host(ip_addr):
    port = PORT
    path = DATA_PATH
    name = ip_addr
    h = Host.create_host(name, path, ip_addr, port)
    h = h.to_json() if h else None
    return h

def get_hosts():
    hosts = Host.list()
    hosts = [h.to_json() for h in hosts] if hosts else None
    return hosts
