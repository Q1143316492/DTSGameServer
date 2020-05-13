# coding=utf-8
import errno
import select
import socket
from server_core.log import Log
from server_core import config
from server_core.network import NetworkServerBase
from server_core.connection_pool import ConnectionPool


class Epoll(NetworkServerBase):

    def __init__(self, port, use_et=False):
        NetworkServerBase.__init__(self, port)

        self.use_et = use_et
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

        if self.use_et is False:
            self.epoll_fd.register(self.server_fd.fileno(), select.EPOLLIN)
        else:
            self.epoll_fd.register(self.server_fd.fileno(), select.EPOLLIN | select.EPOLLET)

    def __accept_client(self):
        if not self.use_et:    # epoll lt
            client_fd = None
            try:
                client_fd, remote = self.server_fd.accept()
            except socket.error as e:
                self.logger.debug("epoll lt accept socket.error " + str(e.errno))
            if not client_fd:
                return
            self.epoll_fd.register(client_fd.fileno(), select.EPOLLIN)
            conn_id = self.conn_pool.add_conn(client_fd)
            self.logger.debug("epoll lt accept: " + str(conn_id))
            self.file_no_to_connections_dict[client_fd.fileno()] = conn_id
        else:   # epoll et
            try:
                while True:
                    client_fd, remote = self.server_fd.accept()
                    if not client_fd:
                        continue
                    self.epoll_fd.register(client_fd.fileno(), select.EPOLLIN | select.EPOLLET)
                    conn_id = self.conn_pool.add_conn(client_fd)
                    self.logger.debug("epoll et accept: " + str(conn_id))
                    self.file_no_to_connections_dict[client_fd.fileno()] = conn_id
            except socket.error as e:
                if e.args[0] not in [errno.EAGAIN, errno.EINTR]:
                    raise

    def __update_readable(self, file_no):
        conn_id = self.file_no_to_connections_dict[file_no]
        # epoll lt
        if not self.use_et:
            is_exit = self.conn_pool.recv_event(conn_id)
            if not is_exit:
                self.epoll_fd.modify(file_no, select.EPOLLOUT)
            else:
                self.__update_client_out(file_no)
        # epoll et
        else:
            is_exit = self.conn_pool.recv_event(conn_id, use_et=True)
            if not is_exit:
                self.epoll_fd.modify(file_no, select.EPOLLOUT | select.EPOLLET)
            else:
                self.__update_client_out(file_no)

    def __update_writable(self, file_no):
        conn_id = self.file_no_to_connections_dict[file_no]
        is_empty = self.conn_pool.trigger_send_event(conn_id)
        if is_empty:
            if not self.use_et:
                self.epoll_fd.modify(file_no, select.EPOLLIN)
            else:
                self.epoll_fd.modify(file_no, select.EPOLLIN | select.EPOLLET)

    def __update_client_out(self, file_no):
        self.epoll_fd.unregister(file_no)
        conn_id = self.file_no_to_connections_dict[file_no]
        self.conn_pool.trigger_connection_out_event(conn_id)
        del self.file_no_to_connections_dict[file_no]

    def run(self):
        self.state = config.SERVER_RUN
        try:
            while True:
                events = self.epoll_fd.poll(1)
                for file_fd, event in events:
                    if (event & select.EPOLLHUP) or (event & select.EPOLLERR):
                        # 读事件可能和 HUP 同时存在，也就是客户端在上面 EPOLLIN 的时候发现客户端退出以及踢掉了
                        self.__update_client_out(file_fd)
                    elif file_fd == self.server_fd.fileno():
                        self.__accept_client()
                    elif event & select.EPOLLIN:
                        self.__update_readable(file_fd)
                    elif event & select.EPOLLOUT:
                        self.__update_writable(file_fd)
                self.workers.update()

        except KeyboardInterrupt as e:
            # 这个信号是终端 ctrl + c 导致退出，测试环境 linux
            self.logger.error("server out success with KeyboardInterrupt. " + str(e) + " ")
        except IOError as e:
            self.logger.error("server out error. err " + str(e.errno) + " " + e.strerror)
        finally:
            self.epoll_fd.unregister(self.server_fd.fileno())
            self.epoll_fd.close()
            self._close_fd()
