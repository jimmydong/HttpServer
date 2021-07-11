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
    fd = os.popen('ps -ax -o pid,args --columns=200')
    if request.search:
        out = []
        for i in fd.readlines():
            if re.search(request.search, i):
                out.append(i)
    else:
        out = fd.readlines()
    fd.close()
    return util.jsonOk(out)

# 获取服务器信息
def host(request: Request, response: Response):
    out = {}
    fd = os.popen('df -h')
    out['disk'] = fd.read(4096)
    fd.close()

    fd = os.popen('df -h')
    out['iptables'] = os.popen('iptables-save')
    fd.close()

    fd = os.popen('df -h')
    out['rc_local'] = os.popen('cat /etc/rc.local')
    fd.close()

    fd = os.popen('df -h')
    out['crontab'] = os.popen('crontab -l')
    fd.close()
    
    print(out)

    return util.jsonOk(out)


if __name__ == '__main__':
    request = Request({}, {'search':'/Google Chrome.app/|/User/'}, {})
    response = Response({'_c':'shell', '_a':'ps'})
    debug(f"__{response._c}__:", eval(response._a)(request, response))