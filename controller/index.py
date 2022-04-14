# -*- coding:utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util import debug

from root.index import Request, Response

def index(request: Request, response: Response):
    out = "403 Forbidden: "
    out += f"by laodong, v0.0.1"
    return out

if __name__ == '__main__':
    request = Request({}, {'foo':'bar'}, {})
    response = Response({'_c':'index', '_a':'index'})
    debug(f"__{response._c}__:", eval(response._a)(request, response))