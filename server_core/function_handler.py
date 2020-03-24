# coding=utf-8
from server_core.log import Log


class FunctionHandler:

    def __init__(self, handler_id, handler):
        self.handler_id = handler_id
        self.pre_handler = None
        self.handler = handler
        self.last_handler = None

        if not isinstance(self.handler_id, int) or not callable(handler):
            raise Exception("function handler style error")

        self.logger = Log()

    def set_pre_handler(self, handler):
        if callable(handler):
            self.pre_handler = handler

    def set_last_handler(self, handler):
        if callable(handler):
            self.last_handler = handler

    def run(self, req, res):
        if callable(self.pre_handler):
            self.pre_handler(req, res)
        self.handler(req, res)
        if callable(self.last_handler):
            self.last_handler(req, res)


