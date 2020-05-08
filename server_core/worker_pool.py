# coding=utf-8
from server_core.log import Log
from server_core import config
from server_core.net_request import Request
from server_core.net_response import Response
from server_core.function_handler import FunctionHandler
from server_core.memcache import MemCache
from server_core.event_controller import EventController
import multiprocessing
import Queue
import random


# def worker_function(req, response_queue):
#     response_queue.put(1)
#     pass
# pass
# tools = process_dict["tools"]
# cache = MemCacheMultiProcess()
# process_dict["tools"] = cache
# print id(cache)
# while True:
#     req = request_queue.get()  # 工作进程阻塞等待 request
#     res = Response(req.conn_id)
#     handler = req.get_handler()
#     if handler in handler_dict.keys():  # 根据 request 哈希到具体函数
#         handler_dict[handler].run(tools, req, res)
#         response_queue.put(res)         # 如果满了会阻塞，尽量避免阻塞, response 尽快消费


class CommonTools:

    def __init__(self):
        self.mem_cache = None
        self.handler_dict = None
        self.events = None

    def init(self, handler_dict):
        self.mem_cache = MemCache()
        self.handler_dict = handler_dict
        self.events = EventController(handler_dict=self.handler_dict)

        self.mem_cache.set(config.GLOBAL_TOOLS, self)
        self.mem_cache.set(config.GLOBAL_FUNC_DICT, self.handler_dict)
        self.mem_cache.set(config.GLOBAL_EVENT_TOOLS, self.events)

    def update(self):
        self.events.update()


class WorkerPool:

    def __init__(self, mode=None):
        self.mode = mode  # 默认使用单进程单线程模式
        self.logger = Log()
        self.conn_pool = None

        # key = id, value = FunctionHandler. int 到函数的映射
        self.handler_dict = {}
        # 通用工具集
        self.common_tools = CommonTools()

        # TODO 多进程 删掉了 并没有什么用
        self.process_count = 1
        self.process_pool = None
        # 单进程模式下处理完的事件丢到这里，后面主循环处理发回客户端
        self.response_queue = []
        self.auto_incr = 0

    def init(self, conn_pool, process_count=4):
        self.conn_pool = conn_pool
        if process_count < 1 or process_count > 10:
            process_count = 1
        self.process_count = process_count

    def start(self):
        self.common_tools.init(self.handler_dict)
        self.logger.info("worker pool. light mode")
        self.logger.info("work process start success")

    def stop(self):
        pass

    def add_handler(self, handler, controller):
        if isinstance(handler, int) and isinstance(controller, FunctionHandler):
            self.handler_dict[handler] = controller

    def del_handler(self, handler):
        if handler in self.handler_dict.keys():
            del self.handler_dict[handler]

    # 在框架IO层，处理好 [消息] 后调用.
    # 需要路由到具体逻辑代码
    # 最后调用 self.conn_pool.send_event(conn_id, res)， res 会在合适的时候发给客户端
    def message_handler(self, conn_id, msg):
        req = Request(conn_id, msg)
        res = Response(conn_id)
        handler = req.get_handler()
        if handler in self.handler_dict.keys():  # 根据 request 哈希到具体函数
            self.handler_dict[handler].run(self.common_tools, req, res)
            self.response_queue.append(res)

    def update(self):
        self.common_tools.update()
        self.message_consumer()

    # 消费处理好的 response，发向客户端
    def message_consumer(self):
        if len(self.response_queue):
            res = self.response_queue[0]
            self.response_queue = self.response_queue[1:]
            self.conn_pool.send_handler(res.conn_id, res.msg)
