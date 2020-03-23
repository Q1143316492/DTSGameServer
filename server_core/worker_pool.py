# coding=utf-8
from server_core.log import Log
from server_core.net_request import Request
from server_core.net_response import Response
import multiprocessing


class WorkerPool:

    def __init__(self):
        self.logger = Log()
        self.conn_pool = None
        self.handler_dict = {}

    def init(self, conn_pool):
        self.conn_pool = conn_pool

    def add_handler(self, handler, controller):
        if isinstance(handler, int) and callable(controller):
            self.handler_dict[handler] = controller

    def del_handler(self, handler):
        if handler in self.handler_dict.keys():
            del self.handler_dict[handler]

    # 在框架IO层，处理好 [消息] 后调用.
    # 需要路由到具体逻辑代码
    # 最后调用 self.conn_pool.send_event(conn_id, res)， res 会在合适的时候发给客户端
    def message_handler(self, conn_id, msg):
        req = Request(msg)
        res = Response()
        handler = req.get_handler()

        if handler in self.handler_dict.keys():
            self.handler_dict[handler](req, res)
            # self.process_pool.map(self.handler_dict[handler], )

        self.conn_pool.send_handler(conn_id, res.msg)