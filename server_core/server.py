# coding=utf-8
import platform
import select
from server_core.log import Log
from server_core.config import *
from server_core.worker_pool import WorkerPool
from server_core.network_nio import LightServer
from server_core.network_select import Select
from server_core.network_epoll import Epoll


class Server:

    def __init__(self, name, uuid):
        self.os_name = platform.system()
        self.python_version = platform.python_version().split(".")[0]

        self.server_name = name
        self.server_id = uuid

        self.network_server = None
        self.work_process = None
        self.logger = Log()

    def add_handler(self, handler_func):
        try:
            self.work_process.add_handler(handler_func.handler_id, handler_func)
            self.logger.info("add handler " + str(handler_func.handler_id))
        except Exception as e:
            self.logger.error("work process not init." + e.message)

    # 预选择服务器IO模式
    def pre_bind_io_mode(self, port, mode):
        if not isinstance(mode, str):
            return False
        if mode.__eq__("epoll") and hasattr(select, 'epoll'):
            self.network_server = Epoll(port)
            self.logger.info("network mode epoll")
            return True
        if mode.__eq__("epoll_et") and hasattr(select, 'epoll'):
            self.network_server = Epoll(port, use_et=True)
            self.logger.info("network mode epoll et")
            return True
        if mode.__eq__("select") and hasattr(select, 'select'):
            self.network_server = Select(port)
            self.logger.info("network mode select")
            return True
        if mode.__eq__("light"):
            self.network_server = LightServer(port)
            self.logger.info("network mode light server")
            return True
        return False

    def start(self, port=7736, mode=None):

        if not self.pre_bind_io_mode(port, mode):
            if hasattr(select, 'epoll'):
                self.network_server = Epoll(port)
                self.logger.info("network mode epoll lt")
            elif hasattr(select, 'select'):
                self.network_server = Select(port)
                self.logger.info("network mode select")
            else:
                self.network_server = LightServer(port)
                self.logger.info("network mode light server")

        self.work_process = WorkerPool()

        self.network_server.init(self.work_process)
        self.work_process.init(self.network_server.conn_pool)

        self.network_server.start()

    def run(self):
        if self.network_server is None:
            self.logger.error("server instance is None")
            return
        if self.network_server.state == SERVER_ESTABLISHED:
            self.work_process.start()
            self.network_server.run()

    def stop(self):
        self.work_process.stop()
