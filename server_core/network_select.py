# coding=utf-8
import select
import socket
from server_core.log import Log
from server_core import config
from server_core.network import NetworkServerBase
from server_core.connection_pool import ConnectionPool


class Select(NetworkServerBase):

    def __init__(self, port=0):
        NetworkServerBase.__init__(self, port)

        self.inputs = []
        self.outputs = []
        self.readable = None
        self.writable = None
        self.exceptional = None

        self.mode = config.SERVER_MODE_SELECT
        self.workers = None
        self.conn_pool = ConnectionPool()
        self.socket_to_conn_id_dict = {} # key: socket val conn_id

    def init(self, workers):
        self.workers = workers
        self.workers.init(self.conn_pool)
        self.conn_pool.init(self.workers, self.mode)

    def start(self):
        self._network_start()

    def __accept_client(self):
        client_fd = None
        try:
            client_fd, remote = self.server_fd.accept()
        except Exception as e:
            pass
        if not client_fd:
            return
        self.inputs.append(client_fd)
        conn_id = self.conn_pool.add_conn(client_fd)
        self.socket_to_conn_id_dict[client_fd] = conn_id

    def __update_readable(self):
        for s in self.readable:
            if s is self.server_fd:
                # 客户端接入
                self.__accept_client()
            else:
                conn_id = self.socket_to_conn_id_dict[s]
                is_exit = self.conn_pool.recv_event(conn_id)
                # 需要读数据，分两种情况
                # 【1】如果读的时候发现客户端还活着，要把句柄加入写事件的监听
                if not is_exit and s not in self.outputs:
                    self.outputs.append(s)
                # 【2】如果读的时候发现客户端死了，要收尾
                else:
                    if s in self.outputs:
                        self.outputs.remove(s)
                    self.inputs.remove(s)
                    self.conn_pool.trigger_connection_out_event(conn_id)
                    if s in self.socket_to_conn_id_dict.keys():
                        del self.socket_to_conn_id_dict[s]

    def __update_writable(self):
        for s in self.writable:
            if s not in self.socket_to_conn_id_dict.keys():
                self.outputs.remove(s)
                continue
            conn_id = self.socket_to_conn_id_dict[s]
            is_empty = self.conn_pool.trigger_send_event(conn_id)
            if is_empty:
                self.outputs.remove(s)

    def __update_exceptional(self):
        for s in self.exceptional:
            self.inputs.remove(s)
            if s in self.socket_to_conn_id_dict.keys():
                conn_id = self.socket_to_conn_id_dict[s]
                self.conn_pool.trigger_connection_out_event(conn_id)
                del self.socket_to_conn_id_dict[s]
            if s in self.outputs:
                self.outputs.remove(s)

    def run(self):
        self.state = config.SERVER_RUN
        self.inputs.append(self.server_fd)
        while self.inputs:
            self.readable, self.writable, self.exceptional = select.select(self.inputs, self.outputs, self.inputs)
            self.__update_readable()
            self.__update_writable()
            self.__update_exceptional()
