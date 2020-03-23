# coding=utf-8
import socket
from server_core import config
from server_core.log import Log


class NetworkServerBase:

    def __init__(self, port):
        self.host = "0.0.0.0"
        self.port = port
        self.server_fd = None
        self.state = config.SERVER_STOP
        self.logger = Log()

    def _close_fd(self):
        try:
            self.server_fd.shutdown(socket.SHUT_RDWR)
            self.server_fd.close()
        except IOError as e:
            self.logger.error("net socket close fail err: " + str(e.errno) + " " + e.strerror)

    def _network_start(self):
        self.server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_fd.bind((self.host, self.port))
        except IOError as e:
            self._close_fd()
            self.logger.error("server bind fail. msg: " + str(e.errno) + " " + e.strerror)
            return

        self.server_fd.listen(config.MAX_LISTEN_QUEUE_SIZE)
        self.server_fd.setblocking(False)
        self.port = self.server_fd.getsockname()[1]
        self.state = config.SERVER_ESTABLISHED
        self.logger.info("server established. port:" + str(self.port))