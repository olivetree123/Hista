#coding:utf-8
import os
from datetime import datetime
from peewee import CharField, BooleanField
from playhouse.postgres_ext import BinaryJSONField

from models import BaseModel
from config import DATA_PATH

class Bucket(BaseModel):
    name = CharField(unique=True, null=False, help_text="bucket name")
    path = CharField(unique=True, null=False, help_text="folder path")
    desc = CharField(null=True, help_text="description")
    public = BooleanField(default=False, null=False, help_text="is public or not")
    extra_info = BinaryJSONField(null=True, help_text="user defined infomation")

    @classmethod
    def add(cls, name, public=True, status=True, desc=None, extra_info=None):
        try:
            public = True if public else False
            path = os.path.join(DATA_PATH, name)
            b = cls.create(name=name, path=path, public=public, status=status, desc=desc, extra_info=extra_info)
        except Exception as e:
            print(e)
            b = None
        return b
    
    @classmethod
    def renew(cls, name, public=None, desc=None, extra_info=None):
        b = cls.get_by_name(name)
        if not b:
            return None
        if public in [0, 1]:
            b.public = public
        if not desc is None:
            b.desc = desc
        b.extra_info = extra_info
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
    
    @classmethod
    def filter_bucket(cls, status=True, **kwargs):
        r = cls.select().where(cls.status == status)
        for key, value in kwargs.items():
            r = r.where(cls.extra_info[key] == value)
        return r.execute()

    def to_json(self):
        r = super(Bucket, self).to_json()
        extra_info = r.pop("extra_info")
        if not extra_info:
            return r
        for key, value in extra_info.items():
            r[key] = value
        return r        