import os

result = os.popen('su -c "%s" root' % 'ps -af -o args --columns=200')
for i in result.readlines():
    print(i)
