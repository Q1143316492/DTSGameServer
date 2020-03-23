# coding=utf-8
import select
import socket
from server_core.log import Log
from server_core import config
from server_core.network import NetworkServerBase
from server_core.connection_pool import ConnectionPool


class Epoll(NetworkServerBase):

    def __init__(self, port):
        NetworkServerBase.__init__(self, port)

        self.mode = config.SERVER_MODE_EPOLL
        self.workers = None
        self.conn_pool = ConnectionPool()
        self.file_no_to_connections_dict = {}  # key: file no val: connection
        self.epoll_fd = None

    def init(self, workers):
        self.workers = workers
        self.workers.init(self.conn_pool)
        self.conn_pool.init(self.workers, self.mode)

    def start(self):
        self._network_start()
        self.epoll_fd = select.epoll()
        self.epoll_fd.register(self.server_fd.fileno(), select.EPOLLIN)

    def __accept_client(self):
        client_fd = None
        try:
            client_fd, remote = self.server_fd.accept()
        except Exception as e:
            pass
        if not client_fd:
            return
        self.epoll_fd.register(client_fd.fileno(), select.EPOLLIN)
        conn_id = self.conn_pool.add_conn(client_fd)
        print "accept: " + str(conn_id)
        self.file_no_to_connections_dict[client_fd.fileno()] = conn_id

    def __update_readable(self, file_no):
        conn_id = self.file_no_to_connections_dict[file_no]
        is_exit = self.conn_pool.recv_event(conn_id)
        if not is_exit: # 接下来要监听此句柄的可写
            self.epoll_fd.modify(file_no, select.EPOLLOUT)
        else: # 发现这个客户端挂了，要收尾
            self.conn_pool.trigger_connection_out_event(conn_id)
            del self.file_no_to_connections_dict[file_no]

    def __update_writable(self, file_no):
        conn_id = self.file_no_to_connections_dict[file_no]
        is_empty = self.conn_pool.trigger_send_event(conn_id)
        if is_empty:
            self.epoll_fd.modify(file_no, select.EPOLLIN)

    def __update_client_out(self, file_no):
        self.epoll_fd.unregister(file_no)
        conn_id = self.file_no_to_connections_dict[file_no]
        print "client out" + conn_id
        self.conn_pool.trigger_connection_out_event(conn_id)
        del self.file_no_to_connections_dict[file_no]

    def run(self):
        self.state = config.SERVER_RUN
        try:
            while True:
                events = self.epoll_fd.poll(1)
                for file_fd, event in events:
                    if file_fd == self.server_fd.fileno():
                        self.__accept_client()
                    elif event & select.EPOLLIN:
                        self.__update_readable(file_fd)
                    elif event & select.EPOLLOUT:
                        self.__update_writable(file_fd)
                    elif event & select.EPOLLHUP:
                        self.logger.info("epoll hub")
                        self.__update_client_out(file_fd)
        except KeyboardInterrupt as e:
            self.logger.error("server out success with KeyboardInterrupt. " + str(e) + " ")
        except IOError as e:
            self.logger.error("server out error. err " + str(e.errno) + " " + e.strerror)
        finally:
            self.epoll_fd.unregister(self.server_fd.fileno())
            self.epoll_fd.close()
            self._close_fd()

