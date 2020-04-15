# _*_coding:utf-8_*_
import socket
import errno
from server_core.log import Log
from server_core.message import Message


class Connection:
    err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
    err_conn = (errno.EISCONN, 10057, 10035)  # client 10053

    def __init__(self, workers):
        self.client_fd = None
        self.recv_buf = ''
        self.send_buf = ''
        self.conn_id = None
        self.msg = Message()
        self.logger = Log()
        self.workers = workers

    def close_fd(self):
        try:
            self.logger.debug(
                "client exit. fd = " + str(self.client_fd) + "port = " + str(self.client_fd.getpeername()[1]))
            self.client_fd.shutdown(socket.SHUT_RDWR)
            self.client_fd.close()
        except IOError as err:
            self.logger.error("conn socket close fail err:" + str(err.errno))

    def assign(self, fd, conn_id):
        self.client_fd = fd
        self.client_fd.setblocking(False)
        self.client_fd.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.conn_id = conn_id
        self.logger.debug("new client. fd = " + str(self.client_fd) + "port = " + str(self.client_fd.getpeername()[1]))

    def _package_message(self):
        while len(self.recv_buf) != 0:
            size = self.msg.recv(self.recv_buf)
            self.recv_buf = self.recv_buf[size:]
            if self.msg.finish():
                # self.logger.debug("recv msg" + self.msg.__str__())
                self.workers.message_handler(self.conn_id, self.msg)
                self.msg.assign()

    def recv_event(self):
        text = ''
        # 客户端退出 not text为 True，这里text上空字符串。
        # 如果是客户端暂时没有数据，并不会导致text为空传，导致10035异常，非阻塞模式中
        try:
            text = self.client_fd.recv(1024)
            if not text:
                err_code = 10000
                self.close_fd()
                return True
        except socket.error, (code, strerror):
            if code not in Connection.err_d:
                err_code = code
                self.close_fd()
                return True
        self.recv_buf += text
        self._package_message()
        return False

    def recv_event_epoll_et(self):
        text = ''
        client_out = False # 用于标记客户端可能异常，需要手动掐掉
        try:
            while True:
                text = self.client_fd.recv(1024)
                if not text:
                    err_code = 10000
                    self.close_fd()
                    return True
                self.recv_buf += text
                # et 模式下收大量数据，客户端可能有bug。放弃此连接
                if len(self.recv_buf) > 10240:
                    client_out = True
                    break
        except socket.error, (code, strerror):
            if code not in Connection.err_d:
                err_code = code
                self.close_fd()
                return True
        if not text or client_out:
            err_code = 10000
            self.close_fd()
            return True
        self._package_message()
        return False

    def send_event(self):
        if isinstance(self.send_buf, str):
            self.client_fd.sendall(self.send_buf)
