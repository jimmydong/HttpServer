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
    t = []
    for i in fd.readlines():
        t.append(i)
    out['disk'] = t
    fd.close()

    fd = os.popen('cat /etc/rc.local')
    t = []
    for i in fd.readlines():
        t.append(i)
    out['rc_local'] = t
    fd.close()

    fd = os.popen('sudo iptables-save')
    t = []
    for i in fd.readlines():
        t.append(i)
    out['iptables'] = t
    fd.close()

    fd = os.popen('sudo crontab -l')
    t = []
    for i in fd.readlines():
        t.append(i)
    out['crontab'] = t
    fd.close()

    fd = os.popen('sudo systemctl list-unit-files --type=service | grep -v disabled')
    t = []
    for i in fd.readlines():
        t.append(i)
    out['systemd'] = t
    fd.close()

    fd = os.popen('sudo cat /etc/passwd')
    t = []
    for i in fd.readlines():
        t.append(i)
    out['passwd'] = t
    fd.close()
    
    return util.jsonOk(out)


if __name__ == '__main__':
    request = Request({}, {'search':'/Google Chrome.app/|/User/'}, {})
    response = Response({'_c':'shell', '_a':'ps'})
    debug("__%s__:" % response._c, eval(response._a)(request, response))