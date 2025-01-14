# -*- coding=utf-8 -*-
from io import StringIO
import socket
import threading
import queue
import os
from HttpHead import HttpRequest


# 每个任务线程
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):     # 生成一些线程来执行任务
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))

# 处理tcp连接
def tcp_link(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    request = sock.recv(4096) # 注意大小限制
    http_req = HttpRequest()
    try:
        http_req.passRequest(request)
        sock.send(http_req.getResponse().encode('utf-8'))
    except Exception as err:
        print('exception: %s' % str(err))
        sock.send('500\r\n500 Internal Server Error'.encode('utf-8'))
    sock.close()

# 启动守护
def start_server():
    bind = '0.0.0.0'
    port = 7788
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((bind, port))
    s.listen(10)
    thread_pool = ThreadPoolManger(5)
    print('listen in %s:%d' % (bind, port))
    while True:
        sock, addr = s.accept()
        thread_pool.add_work(tcp_link, *(sock, addr))


if __name__ == '__main__':
    # PID文件
    curPath = os.path.abspath(os.path.dirname(__file__))
    pid = os.getpid()
    with open('%s/server.pid' % curPath, 'w') as file:
        file.write('%d' % pid)
    # 执行
    start_server()


