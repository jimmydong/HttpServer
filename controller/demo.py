# -*- coding:utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util import debug

from root.index import Request, Response

def test(request: Request, response: Response):
    out = "Test this DEMO : /?_c=demo&_a=test&foo=bar"
    out += f"<br/>\n   foo:{request.foo}"
    return out

if __name__ == '__main__':
    request = Request({}, {'foo':'bar'}, {})
    response = Response({'_c':'demo', '_a':'test'})
    debug("test():", test(request, response))