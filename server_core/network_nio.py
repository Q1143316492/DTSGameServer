# coding=utf-8
import socket
import time
from server_core.log import Log
from server_core import config
from server_core.connection_pool import ConnectionPool
from server_core.network import NetworkServerBase
from server_core.worker_pool import WorkerPool


# 这里 light 是轻量级的意思
class LightServer(NetworkServerBase):

    def __init__(self, port=0):
        NetworkServerBase.__init__(self, port)

        self.mode = config.SERVER_MODE_EASY
        self.workers = None
        self.conn_pool = ConnectionPool()

    def init(self, workers):
        self.workers = workers
        self.workers.init(self.conn_pool)
        self.conn_pool.init(self.workers, self.mode)

    def start(self):
        self._network_start()

    def run(self):
        self.state = config.SERVER_RUN
        while True:
            # time.sleep(0.1)
            self.__accept_client()
            self.__update_client()
            self.workers.message_consumer()

    def __accept_client(self):
        client_fd = None
        try:
            client_fd, remote = self.server_fd.accept()
        except Exception as e:
            pass
        if not client_fd:
            return
        self.conn_pool.add_conn(client_fd)

    def __update_client(self):
        self.conn_pool.update()