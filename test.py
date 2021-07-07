import os

result = os.popen('ps -ef')
for i in result.readlines():
    print(i)
