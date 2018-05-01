#coding:utf-8

from config import PORT
from winney import Winney

def winney_api(host):
    wy = Winney(host=host, port=PORT)
    wy.add_url(method="post", uri="/api/file", function_name="save_file")
    return wy