#coding:utf-8

from peewee import CharField
from datetime import datetime
from models import BaseModel, sqlite_db

class Obj(BaseModel):
    name        = CharField(null=False, index=True, help_text="object name")
    info        = CharField(max_length=500,         help_text="user defined infomation")
    bucket      = CharField(null=False, index=True, help_text="bucket name")
    filename    = CharField(null=False, index=True, help_text="file name")
    md5_hash    = CharField(null=False, index=True, help_text="file hash")
    
    class Meta:
        database = sqlite_db
        indexes = (
            (("name", "bucket"), True),
            (("filename", "bucket"), True),
        )

    @classmethod
    def create_or_update(cls, name, bucket, filename, md5_hash, info=None, status=True):
        obj = cls.get_by_name(bucket, name)
        if obj:
            obj.info     = info
            obj.status   = status
            obj.filename = filename
            obj.md5_hash = md5_hash
            obj.save()
            return obj
        try:
            obj = cls.create(name=name, bucket=bucket, filename=filename, md5_hash=md5_hash, info=info, status=status)
        except Exception as e:
            obj = None
        return obj
    
    @classmethod
    def list_obj(cls, bucket):
        res = cls.select().where(cls.bucket == bucket, cls.status == True)
        return res
    
    @classmethod
    def get_by_name(cls, bucket, name):
        try:
            obj = cls.get(cls.name == name, cls.bucket == bucket)
        except Obj.DoesNotExist:
            obj = None
        return obj
    
    @classmethod
    def remove(cls, bucket, name):
        r = cls.update({cls.status : False}).where(cls.bucket == bucket, cls.name == name).execute()
        return r
    
    @classmethod
    def remove_objs(cls, bucket, name_list):
        r = cls.update({cls.status : False}).where(cls.bucket == bucket, cls.name.in_(name_list)).execute()
        return r

