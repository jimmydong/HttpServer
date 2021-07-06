# -*- coding:utf-8 -*-

from root.index import Request, Response


def index(request: Request, response: Response):
    out = "Hello World"
    out += f"   {response._c}/{response._a}"
    return out
