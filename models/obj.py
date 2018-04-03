#coding:utf-8

from peewee import CharField
from datetime import datetime
from models import BaseModel, sqlite_db

class Obj(BaseModel):
    name = CharField(null=False, index=True, help_text="object name")
    bucket_name = CharField(null=False, index=True, help_text="bucket id")
    filename = CharField(null=False, index=True, help_text="file name")
    md5_hash = CharField(null=False, index=True, help_text="file hash")
    info = CharField(max_length=500, help_text="附加信息")

    class Meta:
        database = sqlite_db
        indexes = (
            (("name", "bucket_name"), True),
            (("filename", "bucket_name"), True),
        )

    @classmethod
    def create_or_update(cls, name, bucket_name, filename, md5_hash, info=None, status=True):
        obj = cls.get_by_name(name, bucket_name)
        if obj:
            obj.filename = filename
            obj.md5_hash = md5_hash
            obj.info = info
            obj.status = status
            obj.save()
            return obj
        try:
            obj = cls.create(name=name, bucket_name=bucket_name, filename=filename, md5_hash=md5_hash, info=info, status=status)
        except Exception as e:
            obj = None
        return obj
    
    @classmethod
    def get_by_name(cls, name, bucket_name):
        try:
            obj = cls.get(cls.name == name, cls.bucket_name == bucket_name)
        except Obj.DoesNotExist:
            obj = None
        return obj
    
    @classmethod
    def remove(cls, bucket_id):
        obj = cls.get_or_none(id == bucket_id)
        if not obj:
            return None
        obj.status = False
        obj.save()
        return obj
