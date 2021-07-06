# -*- coding:utf-8 -*-


# 全局变量
SESSION = None
POST = None
GET = None
REQUEST = None

def app():
    print(REQUEST)
    print("test app")
    return "Hello World!"