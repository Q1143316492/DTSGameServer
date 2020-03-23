# coding=utf-8
import sys
import errno
import socket
import time
import select
import Queue

sys.path.append('../')

from server_core.log import Log
from server_core.server import Server

# How To Use Linux epoll with Python
# http://scotdoyle.com/python-epoll-howto.html

#   on server 10035         on client 10053
#   EAGAIN ， EWOULDBLOCK 也是 EAGAIN
#   EINPROGRESS 非阻塞 connect 第一次 EINPROGRESS 后面都是 EALREADY
#   EISCONN: The socket is already connected
#   10057 sock 没有连接

err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
err_conn = (errno.EISCONN, 10057, 10035)  # 10035

log = Log()

def close(fd):
    try:
        fd.close()
    except Exception as e:
        log.error("test socket close fail err:" + e.message)


def test_epoll_lt():
    # define
    host = "0.0.0.0"
    port = 7736
    # init
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_fd.setblocking(False)

    try:
        server_fd.bind((host, port))
    except Exception as e:
        close(server_fd)
        return

    server_fd.listen(10)
    server_fd.setblocking(False)
    port = server_fd.getsockname()[1]

    log.debug("success bind port %s" % port)
    log.debug("start success")

    epoll = select.epoll()
    epoll.register(server_fd.fileno(), select.EPOLLIN)

    try:
        connections = {}
        requests = {}
        response = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == server_fd.fileno():
                    client_fd, remote = server_fd.accept()
                    client_fd.setblocking(False)
                    epoll.register(client_fd.fileno(), select.EPOLLIN)
                    connections[client_fd.fileno()] = client_fd
                    requests[client_fd.fileno()] = b''
                    response[client_fd.fileno()] = response
                elif event & select.EPOLLIN:
                    pass
                elif event & select.EPOLLOUT:
                    pass
                elif event & select.EPOLLHUP:
                    pass


    finally:
        epoll.unregister(server_fd.fileno())
        epoll.close()
        server_fd.close()


if __name__ == '__main__':
    pass
    test_epoll_lt()



