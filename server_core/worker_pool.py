# coding=utf-8
from server_core.log import Log
from server_core.net_request import Request
from server_core.net_response import Response
from server_core.function_handler import FunctionHandler
from server_core.memcache import MemCacheMultiProcess, MemCacheSingletonProcess
import multiprocessing
import Queue
import random


def worker_function(tools, request_queue, response_queue, handler_dict):
    while True:
        req = request_queue.get()  # 工作进程阻塞等待 request
        res = Response(req.conn_id)
        handler = req.get_handler()
        if handler in handler_dict.keys():  # 根据 request 哈希到具体函数
            handler_dict[handler].run(tools, req, res)
            response_queue.put(res)         # 如果满了会阻塞，尽量避免阻塞, response 尽快消费


class CommonTools:

    def __init__(self):
        self.mem_cache = None
        self.handler_dict = None


class WorkerPool:

    def __init__(self, mode=None):
        self.mode = mode    # 默认使用单进程单线程模式
        self.logger = Log()
        self.conn_pool = None

        # key = id, value = FunctionHandler. int 到函数的映射
        self.handler_dict = {}

        self.common_tools = CommonTools()

        # 多进程模式的，进程池。请求队列和响应队列
        # 主进程把消息放到请求队列，某个进程取队列的消息。处理，丢回响应队列
        # 主循环循环处理 Response 发向对应客户端
        self.work_progress = []
        self.request_queues = []
        self.response_queues = []
        self.process_count = 1

        # 单进程模式下处理完的事件丢到这里，后面主循环处理发回客户端
        self.response_queue = []
        self.auto_incr = 0

    def init(self, conn_pool, process_count=1):
        self.conn_pool = conn_pool
        if process_count < 1 or process_count > 10:
            process_count = 1
        self.process_count = process_count

    def start(self):
        if self.mode == "multi":
            self.logger.info("worker pool multiprocess mode")
            self.common_tools.mem_cache = MemCacheMultiProcess()
            self.common_tools.handler_dict = self.handler_dict
            for i in range(self.process_count):
                request_queue = multiprocessing.Queue(1000)
                self.request_queues.append(request_queue)

                response_queue = multiprocessing.Queue(1000)
                self.response_queues.append(response_queue)

                worker = multiprocessing.Process(
                    target=worker_function, args=(self.common_tools, request_queue, response_queue, self.handler_dict, ))
                worker.start()
                self.logger.info("new process pid:{} start.".format(worker.pid))
                self.work_progress.append(worker)
        else:
            self.logger.info("worker pool. light mode")
            self.common_tools.mem_cache = MemCacheMultiProcess()
            self.common_tools.handler_dict = self.handler_dict

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
        if self.mode == "multi":
            worker_id = random.randint(0, self.process_count - 1)

            for v in self.request_queues:
                print "size: ", v.qsize()

            try:
                self.request_queues[worker_id].put_nowait(Request(conn_id, msg))
            except Queue.Full:
                self.logger.warn("server is almost full")
        else:
            req = Request(conn_id, msg)
            res = Response(conn_id)
            handler = req.get_handler()
            if handler in self.handler_dict.keys():  # 根据 request 哈希到具体函数
                self.handler_dict[handler].run(self.common_tools, req, res)
                self.response_queue.append(res)

    # 消费处理好的 response，发向客户端
    def message_consumer(self):
        if self.mode == "multi":
            for response_queue in self.response_queues:
                try:
                    res = response_queue.get_nowait()
                    self.conn_pool.send_handler(res.conn_id, res.msg)
                except Queue.Empty:
                    pass
        else:
            # 轻量级模式下：IO复用+单进程单线程
            if len(self.response_queue):
                res = self.response_queue[0]
                self.response_queue = self.response_queue[1:]
                self.conn_pool.send_handler(res.conn_id, res.msg)
