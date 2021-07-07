import os

result = os.popen('ps -af -o args --columns=200')
for i in result.readlines():
    print(i)
