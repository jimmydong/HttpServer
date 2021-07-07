import os

result = os.popen('ps -ax -o pid,args --columns=200')
for i in result.readlines():
    print(i)
