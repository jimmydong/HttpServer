# -*- coding:utf-8 -*-
import os
from pprint import pprint as pp
import sys
import time
import json

# 调试函数
def debug(*args):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        current_frame = sys._getframe(1)
        file = os.path.basename(current_frame.f_code.co_filename)
        line = current_frame.f_lineno
        func = current_frame.f_code.co_name
        if len(args) == 0:
            print('%s %s:line %d ---- here!' % (now, file, line))
        elif len(args) == 1:
            print('%s %s:line %d [debug]' % (now, file, line))
            pp(args[0])
            print('------------------------------------------end debug')
        else:
            print('%s %s:line %d 【%s】' % (now, file, line, args[0]))
            for i in args[1:]:
                pp(i)
            print('------------------------------------------end debug')
    except ValueError:
        return 'unknown', 0, 'unknown'

def access_log(url, method):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    curPath = os.path.abspath(os.path.dirname(__file__))
    with open(curPath + "/logs/access.log", 'a') as f:
        f.write('%s [%s] %s' % (now, method, url))

def jsonOk(data = None):
    re = {"success": True, "data": data}
    return json.dumps(re)

def jsonFail(msg = '', data = None):
    re = {"success": False, "msg": msg, "data": data}
    return json.dumps(re)

if __name__ == '__main__':
    debug('测试', {'hello':'world'})