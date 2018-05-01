#coding:utf-8

from flask import Flask
from flask_restful import Resource
from api import api

from config import PORT
# from models.init import init_db

app = Flask(__name__)
api.init_app(app)
# init_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=PORT)