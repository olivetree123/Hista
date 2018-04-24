#coding:utf-8
import os
from datetime import datetime
from peewee import CharField, BooleanField

from models import BaseModel
from config import DATA_PATH

class Bucket(BaseModel):
    name = CharField(unique=True, null=False, help_text="bucket name")
    path = CharField(unique=True, null=False, help_text="folder path")
    info = CharField(help_text="description")
    public = BooleanField(default=False, null=False, help_text="is public or not")

    @classmethod
    def add(cls, name, public=True, status=True, info=None):
        try:
            public = True if public else False
            path = os.path.join(DATA_PATH, name)
            b = cls.create(name=name, path=path, public=public, status=status, info=info)
        except Exception as e:
            print(e)
            b = None
        return b
    
    @classmethod
    def renew(cls, name, public=-1, info=None):
        b = cls.get_by_name(name)
        if not b:
            return None
        if public in [0, 1]:
            b.public = public
        if not info is None:
            b.info = info
        b.save()
        return b
    
    @classmethod
    def list_bucket(cls):
        res = cls.select().where(cls.status == True)
        return res
    
    @classmethod
    def get_by_name(cls, name):
        try:
            b = cls.get(cls.name == name)
        except Bucket.DoesNotExist:
            b = None
        return b
    
    @classmethod
    def remove(cls, name):
        r = cls.update({cls.status : False}).where(cls.name == name).execute()
        return r