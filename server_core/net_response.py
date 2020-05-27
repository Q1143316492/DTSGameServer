# coding=utf-8
from server_core.net_request import Request


class Response(Request):

    def __init__(self, msg=None):
        Request.__init__(self, msg)
        self.msg_queue = []
