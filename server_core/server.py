# coding=utf-8
import platform
import select
from server_core.log import Log
from server_core.config import *
from server_core.worker_pool import WorkerPool
from server_core.network_nio import LightServer
from server_core.network_select import Select


class Server:

    def __init__(self, name, uuid):
        self.os_name = platform.system()
        self.python_version = platform.python_version().split(".")[0]

        self.server_name = name
        self.server_id = uuid

        self.network_server = None
        self.work_process = None
        self.logger = Log()

    def add_handler(self, handler, controller):
        try:
            self.work_process.add_handler(handler, controller)
            self.logger.info("add handler " + str(handler))
        except Exception as e:
            self.logger.error("work process not init." + e.message)

    def start(self, port=7736):
        # todo
        # if hasattr(select, 'epoll'):
        #     pass
        #    return

        if hasattr(select, 'select'):
            self.network_server = Select(port)
            self.logger.info("network mode select")
        else:
            self.network_server = LightServer(port)

        self.work_process = WorkerPool()

        self.network_server.init(self.work_process)
        self.work_process.init(self.network_server.conn_pool)

        self.network_server.start()

    def run(self):
        if self.network_server is None:
            self.logger.error("server instance is None")
            return
        if self.network_server.state == SERVER_ESTABLISHED:
            self.network_server.run()

    def stop(self):
        pass
