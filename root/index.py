# -*- coding:utf-8 -*-
'''
mvc主文件
'''
import os
import sys
import importlib

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util import debug


# 全局变量
SESSION = dict()
POST = dict()
GET = dict()
REQUEST = dict()

class Response():
    _DATA = {}

    def __init__(self, param = {}):
        for k in param:
            object.__getattribute__(self, '_DATA')[k] = param[k]

    def __getattribute__(self, name: str):
        return object.__getattribute__(self, '_DATA').get(name, '')
    
    def __setattr__(self, name: str, value):
        object.__getattribute__(self, '_DATA')[name] = value

class Request():
    _POST = {}
    _GET = {}
    _SESSION = {}

    def __init__(self, post, get, session):
        self._POST = post
        self._GET = get
        self.session = session

    # 获取request值
    def __getattribute__(self, name: str):
        if name in object.__getattribute__(self, '_GET'):
            return object.__getattribute__(self, '_GET')[name]
        elif name in object.__getattribute__(self, '_POST'):
            return object.__getattribute__(self, '_POST')[name]
        else:
            return ''
    
    # 是否为空
    def notNull(self, name: str):
        if object.__getattribute__(self, '_GET').__contains__(name):
            return True
        elif object.__getattribute__(self, '_POST_').__contains__(name):
            return True
        else:
            return False
    
    def get(self, name: str):
        return object.__getattribute__(self, '_GET').get(name, '')
    
    def post(self, name: str):
        return object.__getattribute__(self, '_POST').get(name, '')
    
    def session(self, name: str):
        return object.__getattribute__(self, '_SESSION').get(name, '')

def app():
    request = Request(POST, GET, SESSION)
    _c = request._c if request._c else 'index'
    _a = request._a if request._a else 'index'
    response = Response()
    response._c = _c
    response._a = _a

    # 安全保护(优先使用密码文件)
    key_file = os.path.split(rootPath)[0] + '/http_server_auth.key'
    if os.path.isfile(key_file):
        with open(key_file , 'r') as f:
            key = f.read(32)
    else:
        key = '39d8DE3fdyGBgdd3'
    if _c in ['shell']:
        if request.key != key:
            return "Authorized Fail."

    py = 'controller/' + _c + '.py'
    if not os.path.isfile(py):
        return "Error: controller not found: %s" % py
    controller = importlib.import_module('controller.' + _c)
    return getattr(controller, _a)(request, response)

    
if __name__ == '__main__':
    GET = {'_c': 'index', '_a': 'index', 'foo':'bar'}
    debug("app():", app())