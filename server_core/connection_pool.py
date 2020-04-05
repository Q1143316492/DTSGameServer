# coding=utf-8
from server_core import config
from server_core.connection import Connection
from server_core.log import Log
from server_core.message import Message
from multiprocessing import Queue
import uuid


class ConnectionPool:

    def __init__(self):
        self.connections = {}  # conn_id : connection
        self.auto_id = 0
        self.logger = Log()
        self.workers = None
        self.mode = None
        self.auto_increase = 0
        self.send_queue = {}  # conn_id : Queue { msg1, msg2, ... }

    def init(self, workers, mode):
        self.workers = workers
        self.mode = mode

    def add_conn(self, client_fd):
        conn = Connection(self.workers)
        conn_id = uuid.uuid3(uuid.NAMESPACE_X500, str(self.auto_increase))
        self.auto_increase += 1
        conn.assign(client_fd, conn_id)
        if len(self.connections) < config.NET_CONNECTION_POOL_SIZE:
            self.connections[conn_id] = conn
            self.logger.debug("connection count = " + str(len(self.connections)))
            return conn_id
        else:
            return None

    def update(self):
        exit_conn = []
        for conn_id, conn in self.connections.items():
            is_exit = conn.recv_event()
            if is_exit:
                exit_conn.append(conn.conn_id)
        for conn_id in exit_conn:
            self.__del_conn(conn_id)

    def __del_conn(self, conn_id):
        # 可写的时候，和IO复用异常的时候，都会出现关闭连接，可能会出现重复关闭
        if conn_id in self.send_queue.keys():
            del self.send_queue[conn_id]
        if conn_id in self.connections.keys():
            del self.connections[conn_id]

    # 返回是否有连接退出
    def recv_event(self, conn_id, use_et=False):
        if conn_id in self.connections.keys():
            conn = self.connections[conn_id]
            # epoll et
            if use_et:
                is_exit = conn.recv_event_epoll_et()
            # epoll lt or others
            else:
                is_exit = conn.recv_event()
            if is_exit:
                self.__del_conn(conn.client_fd)
                return True
        return False

    # 如果是普通的 NIO 服务器，直接向客户端发消息
    # 如果用了 IO 复用，放到待发送队列，等待可写事件
    def send_handler(self, conn_id, msg):
        if self.mode == config.SERVER_MODE_EASY:
            self._send_event(conn_id, msg)
        elif self.mode == config.SERVER_MODE_SELECT or self.mode == config.SERVER_MODE_EPOLL:
            if conn_id not in self.send_queue.keys():
                self.send_queue[conn_id] = Queue.Queue()
                self.send_queue[conn_id].put(msg)
            else:
                self.send_queue[conn_id].put(msg)
        else:
            self.logger.warn("server mode not found")

    # 触发发送事件，返回发送消息是否发完
    def trigger_send_event(self, conn_id):
        if conn_id in self.send_queue.keys():
            try:
                msg = self.send_queue[conn_id].get_nowait()
            except Queue.Empty:
                del self.send_queue[conn_id]
                return True
            else:
                self._send_event(conn_id, msg)
                return False

    def trigger_connection_out_event(self, conn_id):
        self.__del_conn(conn_id)

    def _send_event(self, conn_id, msg):
        if msg is None:
            return
        if isinstance(msg, Message):
            msg = msg.get_stream()
        if conn_id in self.connections.keys():
            conn = self.connections[conn_id]
            conn.send_buf = msg
            conn.send_event()
