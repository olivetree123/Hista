#coding:utf-8

from datetime import datetime
from peewee import CharField, IntegerField
from playhouse.postgres_ext import BinaryJSONField

from models import BaseModel, db

class Obj(BaseModel):
    name        = CharField(null=False, index=True, help_text="object name")
    desc        = CharField(null=True,  index=True, help_text="object description")
    bucket      = CharField(null=False, index=True, help_text="bucket name")
    filename    = CharField(null=False, index=True, help_text="file name")
    md5_hash    = CharField(null=False, index=True, help_text="file hash")
    host_id     = IntegerField(null=False, index=True, help_text="host id")
    extra_info  = BinaryJSONField(null=True,  help_text="user defined infomation")
    
    class Meta:
        database = db
        indexes = (
            (("name", "bucket"), True),
            (("filename", "bucket"), True),
        )

    @classmethod
    def create_or_update(cls, name, bucket, filename, md5_hash, host_id, desc=None, extra_info=None, status=True):
        if extra_info and not isinstance(extra_info, dict):
            return None
        obj = cls.get_by_name(bucket, name)
        if obj:
            obj.desc     = desc
            obj.status   = status
            obj.host_id  = host_id
            obj.filename = filename
            obj.md5_hash = md5_hash
            obj.extra_info = extra_info
            obj.save()
            return obj
        try:
            obj = cls.create(name=name, bucket=bucket, filename=filename, md5_hash=md5_hash, host_id=host_id, desc=desc, extra_info=extra_info, status=status)
        except Exception as e:
            print(e)
            obj = None
        return obj
    
    @classmethod
    def list_obj(cls, bucket, **kwargs):
        res = cls.list().where(cls.bucket == bucket)
        for key, value in kwargs.items():
            res = res.where(cls.extra_info[key] == value)
        return res
    
    @classmethod
    def get_by_name(cls, bucket, name):
        try:
            obj = cls.get(cls.name == name, cls.bucket == bucket)
        except Obj.DoesNotExist:
            obj = None
        return obj
    
    @classmethod
    def remove_by_name(cls, bucket, name):
        r = cls.update({cls.status : False}).where(cls.bucket == bucket, cls.name == name).execute()
        return r
    
    @classmethod
    def remove_objs(cls, bucket, name_list):
        r = cls.update({cls.status : False}).where(cls.bucket == bucket, cls.name.in_(name_list)).execute()
        return r

    def to_json(self):
        r = super(Obj, self).to_json()
        extra_info = r.pop("extra_info")
        if not extra_info:
            return r
        for key, value in extra_info.items():
            r[key] = value
        return r        
