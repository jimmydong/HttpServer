# -*- coding:utf-8 -*-
'''
利用TSC进行远端服务器检查。非通用功能，仅适用特定服务器。
调用参考：
curl -X POST --header "Content-Type: text/plain" 'http://127.0.0.1:7788/review?ip=1.1.1.1&password=kakaka' --data-binary @- << EOF
#!/bin/sh
cd /tmp
pwd
ls -lh
EOF
'''
import os

# 全局变量
SESSION = None
POST = None
GET = None
REQUEST = None
RAW = None

def app():
    tsc_path = '/WORK/TOOLS/tsc_cmd'
    # 判断是否本地测试
    if not os.path.exists(tsc_path):
        tsc_path = '/Users/user/Downloads/tsc_cmd'
    
    # 处理参数
    check_flag = False
    if ('ip' in GET.keys()) and ('password' in GET.keys()):
        ip = GET['ip']
        password = GET['password']
        check_flag = True
    if not check_flag:
        return 'error: no ip or password'
    if not os.path.exists('%s/tsc_cmd' % tsc_path):
        return 'error: no tsc_cmd'
    # 保存脚本
    with open('%s/review_temp.sh' % tsc_path, 'w') as f:
        f.write(RAW)
    # 配置文件
    with open('%s/iplist_temp' % tsc_path, 'w') as f:
        f.write("%s\troot\t%s" % (ip, password))
    
    # 本地测试结束
    if tsc_path.startswith('/Users'):
        return '测试'

    # 传输脚本
    fd = os.popen("cd %s && ./tsc_cmd mupload iplist_temp %s/review_temp.sh /tmp/review_temp.sh 1000 2>&1" % (tsc_path, tsc_path))
    t = []
    for i in fd.readlines():
        t.append(i)
    fd.close()
    ret = "\n".join(t)
    if ret.find('TRANSFER FILE OK') == -1:
        return "Error: 传输错误\n%s" % ret
    
    # 执行脚本
    fd = os.popen("cd %s && ./tsc_cmd mshell %s/iplist_temp 'sh /tmp/review_temp.sh' '' 2>&1" % (tsc_path, tsc_path))
    t = []
    for i in fd.readlines():
        t.append(i)
    fd.close()
    print("\n".join(t))
    ret = t[-1]
    if ret.find('error') == -1:
        return "OK: %s" % ret
    else:
        return "Error: %s" % ret
    