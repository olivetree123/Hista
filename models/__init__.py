#coding:utf-8
import uuid
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from peewee import SqliteDatabase, PostgresqlDatabase, Model, BooleanField, DateTimeField

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB
from utils.functions import field_to_json

db = PostgresqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)

class UUIDField(Field):
    field_type = 'uuid'

    def db_value(self, value):
        return value.hex  # convert UUID to hex string.

    def python_value(self, value):
        return uuid.UUID(value) # convert hex string to UUID


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    uid = UUIDField(null=False, primary_key=True, default=uuid.uuid4)
    status = BooleanField(default=True, null=False, help_text="0 delete, 1 normal")
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(constraints=[SQL("DEFAULT current_timestamp")])

    class Meta:
        database = db
    
    @classmethod
    def get_by_uid(cls, uid):
        return cls.get_or_none(cls.uid == uid, cls.status == True)
    
    @classmethod
    def remove(cls, uid):
        try:
            r = cls.get(cls.uid == uid)
            r.status = False
            r.save()
        except:
            r = None
        return r
    
    @classmethod
    def list(cls):
        res = cls.select().where(cls.status == True)
        return res

    def to_json(self):
        data_dict = model_to_dict(self)
        for k, v in data_dict.items():
            data_dict[k] = field_to_json(v)
        return data_dict
