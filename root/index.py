# -*- coding:utf-8 -*-
import os
import importlib

# 全局变量
SESSION = None
POST = None
GET = dict()
REQUEST = dict()

class Response():
    _DATA = {}

    def __getattribute__(self, name: str):
        return self._DATA.get(name, '')
    
    def __setattr__(self, name: str, value):
        self._DATA[name] = value

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
        if name in self._GET:
            print('here')
            return self._GET['name']
        elif name in self._POST:
            return self._POST['name']
        else:
            return ''
    
    # 是否为空
    def notNull(self, name: str):
        if self._GET.__contains__(name):
            return True
        elif self._POST.__contains__(name):
            return True
        else:
            return False
    
    def get(self, name: str):
        return self._GET.get(name, '')
    
    def post(self, name: str):
        return self._POST.get(name, '')
    
    def session(self, name: str):
        return self._SESSION.get(name, '')

def app():
    request = Request(POST, GET, SESSION)
    _c = request._c if request._c else 'index'
    _a = request._a if request._a else 'index'
    response = Response()
    response._c = _c
    response._a = _a

    py = 'controller/' + _c + '.py'
    if not os.path.isfile(py):
        return f"Error: controller not found: {py}"
    controller = importlib.import_module('controller.' + _c)
    return getattr(controller, _a)(request, response)

    
if __name__ == '__main__':
    _GET = {'_c': 'index', '_a': 'index', 'foo':'bar'}
    app()