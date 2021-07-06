# -*- coding:utf-8 -*-
import os
from pprint import pprint as pp
import sys
import time

# 调试函数
def debug(*args):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        current_frame = sys._getframe(1)
        file = os.path.basename(current_frame.f_code.co_filename)
        line = current_frame.f_lineno
        func = current_frame.f_code.co_name
        if len(args) == 0:
            print(f'{now} {file}:line {line} ---- here!')
        elif len(args) == 1:
            print(f'{now} {file}:line {line} [debug]')
            pp(args[0])
            print('------------------------------------------end debug')
        else:
            print(f'{now} {file}:line {line} 【{args[0]}】')
            for i in args[1:]:
                pp(i)
            print('------------------------------------------end debug')
    except ValueError:
        return 'unknown', 0, 'unknown'

if __name__ == '__main__':
    debug('测试', {'hello':'world'})