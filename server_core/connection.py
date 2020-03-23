# _*_coding:utf-8_*_
import socket
import errno
from server_core import config
from server_core.log import Log
from server_core.message import Message


class Connection:

    err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
    err_conn = (errno.EISCONN, 10057, 10035) # client 10053

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
            self.client_fd.close()
        except Exception as e:
            self.logger.error("conn socket close fail err:" + e.message)

    def assign(self, fd, conn_id):
        self.client_fd = fd
        self.client_fd.setblocking(False)
        self.client_fd.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.conn_id = conn_id
        self.logger.debug("new client. fd = " + str(self.client_fd) + "port = " + str(self.client_fd.getpeername()[1]))

    def recv_event(self):
        text = ''
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

        # message
        while len(self.recv_buf) != 0:
            size = self.msg.recv(self.recv_buf)
            self.recv_buf = self.recv_buf[size:]
            if self.msg.finish():
                # todo pack send message
                self.logger.info("recv msg" + self.msg.__str__())
                self.workers.message_handler(self.conn_id, self.msg)
                self.msg.assign()

        return False

    def send_event(self):
        if isinstance(self.send_buf, str):
            self.client_fd.sendall(self.send_buf)
