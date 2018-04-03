#coding:utf-8

from flask import Flask
from flask_restful import Resource
from api import api

from models import sqlite_db
from models.obj import Obj
from models.bucket import Bucket

app = Flask(__name__)
api.init_app(app)

sqlite_db.create_tables([Obj, Bucket], safe=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)