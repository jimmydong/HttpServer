# -*- coding:utf-8 -*-
'''
TSC任务转接。非通用功能，仅适用特定服务器。
'''
import os

# 全局变量
SESSION = None
POST = None
GET = None
REQUEST = None
RAW = None

#生成随机密码
import random
import string
def genPassword(length):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])

def app():
    check_flag = False
    if POST is not None and len(POST) > 0:
        print("post")
        print(POST)
        if ('ip' in POST.keys()) and ('password' in POST.keys()):
            ip = POST['ip']
            password = POST['password']
            check_flag = True
    else:
        print("get")
        print(GET)
        if ('ip' in GET.keys()) and ('password' in GET.keys()):
            ip = GET['ip']
            password = GET['password']
            check_flag = True
    if not check_flag:
        return 'error: no ip or password'
    if not os.path.exists('/WORK/TOOLS/tsc_cmd/tsc_cmd'):
        return 'error: no tsc_cmd'
    #生成密码： 
    new_password = genPassword(16)
    #配置文件
    with open('/WORK/TOOLS/tsc_cmd/iplist_temp', 'w') as f:
        f.write("%s\troot\t%s" % (ip, password))
    #执行命令
    fd = os.popen("cd /WORK/TOOLS/tsc_cmd && ./tsc_cmd mshell iplist_temp \"echo 'root:%s' | chpasswd\" '' 2>&1" % new_password)
    t = []
    for i in fd.readlines():
        t.append(i)
    fd.close()
    # ret = "\n".join(t)
    ret = t[-1]
    if ret.find('error') == -1:
        return "修改目标服务器: %s, 旧密码: %s, 新密码: %s ———— DONE!" % (ip, password, new_password)
    else:
        return "修改目标服务器: %s, 旧密码: %s, 新密码: %s ———— Error: %s" % (ip, password, new_password, ret)
    