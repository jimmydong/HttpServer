# -*- coding:utf-8 -*-
import os
import xml.dom.minidom
import importlib
import copy
from util import debug
import util

_debug = None #单文件调试开关




# 返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
    PY_NOT_FOUND = "HTTP/1.1 404 Python Not Found\r\n"


# 将字典转成字符串
def dict2str(d):
    s = ''
    for i in d:
        s = s + i+': '+d[i]+'\r\n'
    return s

class Session(object):
    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]
        return None

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)        

    def write2XML(self):
        import xml.dom.minidom as minidom
        dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        for key in self.data:
            node = dom.createElement(key)
            node.appendChild(dom.createTextNode(self.data[key]))
            root.appendChild(node)
        debug(self.cook_file)
        with open(self.cook_file, 'w') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')


class HttpRequest(object):
    RootDir = 'root'
    NotFoundHtml = RootDir+'/404.html'
    CookieDir = 'root/cookie/'

    def __init__(self):
        self.method = None
        self.url = ''
        self.query = ''
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.get_data = dict()
        self.post_data = dict()
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''
        self.session = dict()

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        url_info = header_list[1].split('?')
        self.url = url_info[0]
        if len(url_info) > 1: 
            self.query = url_info[1]
        if self.url == '/':
            self.url = '/index'
        self.protocol = header_list[2]

    def passRequestHead(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val
        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']

    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]     # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)

        url = (self.url + '?' + self.query) if self.query else self.url
        util.access_log(url, self.method)

        # 所有post视为动态请求
        # get如果带参数也视为动态请求
        # !!! 不带参数的get视为静态请求 !!!
        if self.method == 'POST':
            self.request_data = {}
            self.get_data = {}
            self.post_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')   # 每一行是一个字段
            for i in parameters:
                if i=='':
                    continue
                key, val = i.split('=', 1)
                self.post_data[key] = val
            if self.query:        # 含有参数的get
                parameters = self.query.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.get_data[key] = val
            self.request_data = dict(self.get_data.items() + self.post_data.items())
            self.dynamicRequest(HttpRequest.RootDir + self.url + '.py')
        if self.method == 'GET':
            if self.query:        # 含有参数的get
                parameters = self.query.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.get_data[key] = val
                self.request_data = copy.deepcopy(self.get_data)
                self.dynamicRequest(HttpRequest.RootDir + self.url + '.py')
            else:
                self.staticRequest(HttpRequest.RootDir + self.url)

    # 只提供制定类型的静态文件
    def staticRequest(self, path):
        debug('staticRequest', path)
        if not os.path.isfile(path):
            if os.path.isfile(path + '.py'):
                self.dynamicRequest(path + '.py')
            else:
                f = open(HttpRequest.NotFoundHtml, 'r')
                self.response_line = ErrorCode.NOT_FOUND
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
        else:
            extension_name = os.path.splitext(path)[1]  # 扩展名
            extension_set = {'.css', '.html', '.js'}
            if extension_name == '.png':
                f = open(path, 'rb')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'text/png'
                self.response_body = f.read()
            elif extension_name in extension_set:
                f = open(path, 'r')
                self.response_line = ErrorCode.OK
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
            elif extension_name == '.py':
                self.dynamicRequest(path)
            # 其他文件不返回
            else:
                f = open(HttpRequest.NotFoundHtml, 'r')
                self.response_line = ErrorCode.NOT_FOUND
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()

    def processSession(self):
        self.session = Session()
        # 没有提交cookie，创建cookie
        if self.Cookie is None:
            self.Cookie = self.generateCookie()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:            
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()                
            # 当前cookie不存在，自动创建
            else:
                self.Cookie = self.generateCookie()
                cookie_file = self.CookieDir+self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()                
        return self.session


    def generateCookie(self):
        import time, hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie

    def dynamicRequest(self, path):
        debug('synamicRequest', path)
        debug('get', self.get_data)
        debug('post', self.post_data)
        # 如果找不到或者后缀名不是py则输出404
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            debug('file not found', path)
            if _debug:
                self.response_body = f"response: file not found: {path}"
            else:
                f = open(HttpRequest.NotFoundHtml, 'r')
                self.response_line = ErrorCode.PY_NOT_FOUND
                self.response_head['Content-Type'] = 'text/html;chartset=utf-8'
                self.response_body = f.read()
        else:
            # 获取文件名，并且将/替换成.
            file_path = path.split('.', 1)[0].replace('/', '.') #注意：文件名中不能有多余的 . 
            self.response_line = ErrorCode.OK
            m = importlib.import_module(file_path)
            m.SESSION = self.processSession()            
            m.REQUEST = self.request_data
            m.POST = self.post_data
            m.GET = self.get_data
            self.response_body = m.app()            
            self.response_head['Content-Type'] = 'text/html;chartset=utf-8'
            self.response_head['Set-Cookie'] = self.Cookie

    def getResponse(self):
        return self.response_line+dict2str(self.response_head)+'\r\n'+self.response_body


if __name__ == '__main__':
    _debug = True
    request = b'GET /index?_c=c&_a=a HTTP/1.1\r\nHost: 127.0.0.1:9999\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nsec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"\r\nsec-ch-ua-mobile: ?0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7\r\nCookie: 1625566670298\r\n\r\n'
    
    http_req = HttpRequest()
    http_req.passRequest(request)
    print(http_req.response_body)

