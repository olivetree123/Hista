#coding:utf-8
import os
from datetime import datetime
from peewee import CharField, BooleanField

from models import BaseModel
from config import BUCKET_BASE_PATH

class Bucket(BaseModel):
    name = CharField(unique=True, null=False, help_text="bucket name")
    path = CharField(unique=True, null=False, help_text="folder path")
    public = BooleanField(default=False, null=False, help_text="is public or not")

    @classmethod
    def add(cls, name, public=True, status=True):
        try:
            public = True if public else False
            path = os.path.join(BUCKET_BASE_PATH, name)
            b = cls.create(name=name, path=path, public=public, status=status)
        except Exception as e:
            print(e)
            b = None
        return b
    
    @classmethod
    def renew(cls, bucket_id, name="", public=-1):
        try:
            b = cls.get(cls.id == bucket_id)
            if name:
                b.name = name
            if public in [0, 1]:
                b.public = public
            b.save()
        except Bucket.DoesNotExist:
            b = None
        return b
    
    @classmethod
    def list(cls):
        res = cls.select().where(cls.status == True)
        return res
    
    @classmethod
    def get_by_name(cls, name):
        try:
            b = cls.get(cls.name == name)
        except Bucket.DoesNotExist:
            b = None
        return b