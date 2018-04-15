#coding:utf-8
import os
from winney import Winney
from models.host import Host
from storage.api import winney_api

def add_host(ip_addr, path, user, password, name=""):
    if not (ip_addr and path and user and password):
        return None
    if not name:
        name = ip_addr.split(".")[-1]
    host = Host.create(name=name, ip_addr=ip_addr, path=path, username=user, password=password)
    return host

def hista_save(path, content, md5):
    # 根据文件的哈希值对主机数量取余，选择存放的主机。
    host_count = Host.count()
    number = int(md5, 16) % host_count
    if number == 0:
        save(path, content, md5)
        return True
    host_list = Host.list()
    host_list = [h.to_json() for h in host_list]
    host = host_list[number]
    # 使用http发送文件内容，让其他服务器保存
    wy = winney_api(host)
    wy.save_file(data={"md5":md5, "path":path, "content":content})
    if wy.ok:
        return True
    return False

def save(path, content, md5):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, md5), "a") as f:
        f.write(content)

    