#coding:utf-8
import os
import shutil
from config import TMP_DIR
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

def hista_save(chunk_num, bucket_path, content, md5, total_chunk):
    # 根据文件的哈希值对主机数量取余，选择存放的主机。
    host = Host.get_host_by_md5(md5)
    if host.name == "localhost":
        return local_save(chunk_num, bucket_path, content, md5, total_chunk)
    # 使用http发送文件内容，让其他服务器保存
    files = {"file" : content}
    wy = winney_api(host.ip_addr)
    wy.save_file(files=files, data={"md5":md5, "bucket_path":bucket_path, "chunk_num":chunk_num, "total_chunk":total_chunk})
    if wy.ok:
        return True
    return False

def local_save(chunk_num, bucket_path, content, md5, total_chunk):
    tmp_dir = os.path.join(bucket_path, TMP_DIR.format(md5))
    if chunk_num == 1 and not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    elif chunk_num > 1 and not os.path.exists(tmp_dir):
        raise Exception("tmp_dir not found, md5 = {} and chunk_num = {}".format(md5, chunk_num))
    with open(os.path.join(tmp_dir, str(chunk_num)), "wb") as f:
        f.write(bytes(content, encoding = "latin-1"))
    if chunk_num == total_chunk:
        return package_file(bucket_path, md5, total_chunk)
    return True

def package_file(bucket_path, md5, total_chunk):
    # 将分片的文件进行组装
    tmp_dir = os.path.join(bucket_path, TMP_DIR.format(md5))
    target_file = os.path.join(bucket_path, md5)
    if not os.path.exists(tmp_dir):
        return False
    if os.path.exists(target_file):
        return True
    f = open(target_file, "ab")
    for i in range(1, total_chunk+1):
        try:
            with open(os.path.join(tmp_dir, str(i)), "rb") as tmp:
                content = tmp.read()
        except Exception as e:
            print(e)
            return False
        f.write(content)
    f.close()
    shutil.rmtree(tmp_dir)
    return True