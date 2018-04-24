#coding:utf-8

from flask import Flask
from flask_restful import Resource
from api import api

from config import PORT
from models import db
from models.obj import Obj
from models.host import Host
from models.bucket import Bucket

app = Flask(__name__)
api.init_app(app)

db.create_tables([Obj, Bucket, Host], safe=True)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)