#coding:utf-8

from models import db
from models.obj import Obj
from models.host import Host
from models.bucket import Bucket
from config import DATA_PATH

def init_db():
    db.create_tables([Obj, Bucket, Host], safe=True)
    h = Host.update_path(name="localhost", path=DATA_PATH)
    if h:
        return
    h = Host.create_host(name="localhost", path=DATA_PATH, ip_addr="localhost")
    msg = "Init host success !" if h else "Error: init host failed !"
    print(msg)
    