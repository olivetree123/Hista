#coding:utf-8

from peewee import CharField
from datetime import datetime
from models import BaseModel, sqlite_db

class Host(BaseModel):
    name     = CharField(help_text="host name")
    path     = CharField(help_text="folder path for stroge")
    status   = BooleanField(default=1, help_text="password")
    ip_addr  = CharField(help_text="ip address")
    username = CharField(null=False, help_text="user name")
    password = CharField(null=False, help_text="password")

    @classmethod
    def list(cls):
        hosts = cls.select().where(cls.status == True)
        return hosts
    
    @classmethod
    def count(cls):
        return cls.select().where(cls.status == True).count()
        
