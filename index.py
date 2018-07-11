#coding:utf-8

from flask import Flask
from multiprocessing import Process
from flask_restful import Resource
from flask_script import Manager, Command, Option

from api import api
from config import PORT
from models.init import init_db
from commands.server import AddServer

app = Flask(__name__)
api.init_app(app)

init_db()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

process = Process(target=sync_data)
process.start()

manager = Manager(app)
manager.add_command("server", AddServer())

if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True, port=PORT)
    manager.run()
    