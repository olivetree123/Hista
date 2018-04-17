#coding:utf-8

from winney import Winney

def winney_api(host):
    wy = Winney(host=host)
    wy.add_url(method="post", url="/api/file", function_name="save_file")
    return wy