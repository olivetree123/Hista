#coding:utf-8

from peewee import CharField, BooleanField
from datetime import datetime
from models import BaseModel

class Host(BaseModel):
    name     = CharField(unique=True, help_text="host name")
    path     = CharField(help_text="folder path for stroge")
    status   = BooleanField(default=1, help_text="password")
    ip_addr  = CharField(unique=True, help_text="ip address")
    username = CharField(null=True, help_text="username")
    password = CharField(null=True, help_text="password")

    @classmethod
    def create_host(cls, name, path, ip_addr, username=None, password=None):
        try:
            host = cls.create(name=name, path=path, status=True, ip_addr=ip_addr, username=username, password=password)
        except Exception as e:
            print(e)
            return None
        return host

    @classmethod
    def list(cls):
        hosts = cls.select().where(cls.status == True)
        return hosts
    
    @classmethod
    def count(cls):
        return cls.select().where(cls.status == True).count()
        
    @classmethod
    def get_host_by_md5(cls, md5):
        host_count = cls.count()
        number = int(md5, 16) % host_count
        host_list = cls.list()
        return host_list[number]

    @classmethod
    def update_path(cls, name, path):
        try:
            host = cls.get_or_none(cls.name == name)
        except:
            return None
        if not host or host.path == path:
            return host
        host.path = path
        host.save()
        return host

