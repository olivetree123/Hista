#coding:utf-8

from datetime import datetime
from playhouse.shortcuts import model_to_dict
from peewee import SqliteDatabase, PostgresqlDatabase, Model, BooleanField, DateTimeField

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_DB
from utils.functions import field_to_json

db = PostgresqlDatabase(MYSQL_DB, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD)

class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    status = BooleanField(default=True, null=False, help_text="0 delete, 1 normal")
    create_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db
    
    @classmethod
    def remove(cls, id):
        try:
            r = cls.get(cls.id == id)
            r.status = False
            r.save()
        except:
            r = None
        return r
    
    @classmethod
    def list(cls):
        res = cls.select(cls.status == True)
        return res

    def to_json(self):
        data_dict = model_to_dict(self)
        for k, v in data_dict.items():
            data_dict[k] = field_to_json(v)
        return data_dict
