# -*- coding:utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from util import debug
import util

from root.index import Request, Response
import re

# 获取进程信息
def ps(request: Request, response: Response):
    result = os.popen('ps -ax -o pid,args --columns=200')
    if request.search:
        out = []
        for i in result.readlines():
            if re.search(request.search, i):
                out.append(i)
    else:
        out = result.readlines()
    return util.jsonOk(out)

# 获取服务器信息
def host(request: Request, response: Response):
    out = {}
    out.disk = os.popen('df -h')
    out.iptables = os.popen('sudo iptables-save')
    out.rc_local = os.popen('sudo cat /etc/rc.local')
    out.crontab = os.popen('sudo crontab -l')
    
    return util.jsonOk(out)


if __name__ == '__main__':
    request = Request({}, {'search':'/Google Chrome.app/|/User/'}, {})
    response = Response({'_c':'shell', '_a':'ps'})
    debug(f"__{response._c}__:", eval(response._a)(request, response))