# coding=utf-8
from server_core.log import Log
from server_core.net_request import Request
from server_core.net_response import Response
from server_core.function_handler import FunctionHandler
import multiprocessing
import Queue
import random


def worker_function(request_queue, response_queue, handler_dict):
    while True:
        req = request_queue.get()  # 工作进程阻塞等待 request
        res = Response(req.conn_id)
        handler = req.get_handler()
        if handler in handler_dict.keys():  # 根据 request 哈希到具体函数
            try:
                handler_dict[handler].run(req, res)
            except Exception as e:
                logger = Log()
                logger.error("service error. handler" + handler)
                logger.error("req: " + str(req.msg))
                logger.error("err: " + str(e))
            response_queue.put(res)         # 如果满了会阻塞，尽量避免阻塞, response 尽快消费


class WorkerPool:

    def __init__(self, mode=None):
        self.mode = mode
        self.logger = Log()
        self.conn_pool = None

        # key = id, value = FunctionHandler. int 到函数的映射
        self.handler_dict = {}

        # 多进程模式的，进程池。请求队列和响应队列
        # 主进程把消息放到请求队列，某个进程取队列的消息。处理，丢回响应队列
        # 主循环循环处理 Response 发向对应客户端
        self.work_progress = []
        self.request_queues = []
        self.response_queues = []
        self.process_count = 1

        # 单进程模式下处理完的事件丢到这里，后面主循环处理发回客户端
        self.response_queue = []

    def init(self, conn_pool, process_count=1):
        self.conn_pool = conn_pool
        self.process_count = process_count

    def start(self):
        if self.mode is None:
            self.logger.info("worker pool. light mode")
        else:
            self.logger.info("worker pool multiprocess mode")
            for i in range(self.process_count):
                request_queue = multiprocessing.Queue(100)
                self.request_queues.append(request_queue)

                response_queue = multiprocessing.Queue(100)
                self.response_queues.append(response_queue)

                worker = multiprocessing.Process(
                    target=worker_function, args=(request_queue, response_queue, self.handler_dict, ))
                worker.start()
                self.work_progress.append(worker)

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
        if self.mode is None:
            req = Request(conn_id, msg)
            res = Response(conn_id)
            handler = req.get_handler()
            if handler in self.handler_dict.keys():  # 根据 request 哈希到具体函数
                self.handler_dict[handler].run(req, res)
                self.response_queue.append(res)
        else:
            worker_id = random.randint(0, self.process_count - 1)
            try:
                self.request_queues[worker_id].put_nowait(Request(conn_id, msg))
            except Queue.Full:
                self.logger.warn("server is almost full")

    # 消费处理好的 response，发向客户端
    def message_consumer(self):
        if self.mode is None:
            if len(self.response_queue):
                res = self.response_queue[0]
                self.response_queue = self.response_queue[1:]
                self.conn_pool.send_handler(res.conn_id, res.msg)
        else:
            for response_queue in self.response_queues:
                try:
                    res = response_queue.get_nowait()
                    self.conn_pool.send_handler(res.conn_id, res.msg)
                except Queue.Empty:
                    pass
