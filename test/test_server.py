# coding=utf-8
import errno
import logging
import socket
import time

from server_core.log import Log
from server_core.server import Server

#   on server 10035         on client 10053
#   EAGAIN ， EWOULDBLOCK 也是 EAGAIN
#   EINPROGRESS 非阻塞 connect 第一次 EINPROGRESS 后面都是 EALREADY
#   EISCONN: The socket is already connected
#   10057 sock 没有连接

err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
err_conn = (errno.EISCONN, 10057, 10035) # 10035

log = Log()

clients = []


def close(fd):
    try:
        fd.close()
    except Exception as e:
        log.error("socket close fail err:" + e.message)
    clients.remove(fd)


def server_temple_recv(client_fd):
    recv_buf = ''
    while True:
        text = ''
        try:
            text = client_fd.recv(1024)
            if not text:
                err_code = 10000
                close(client_fd)
                return -1
        except socket.error, (code, strerror):
            if code not in err_d:
                err_code = code
                close(client_fd)
                return -1
        if text == '':
            break
        recv_buf = recv_buf + text
    return recv_buf


def server_temple_send(client_fd, send_buf):
    try:
        client_fd.sendall(send_buf)
    except socket.error, (code, strerror):
        if code not in err_d:
            err_code = code
            client_fd.close()
            return -1


def accept_client(server_fd):
    client_fd = None
    try:
        client_fd, remote = server_fd.accept()
        print "accept client "
        client_fd.setblocking(False)
    except Exception as e:
        pass
    if not client_fd:
        return
    clients.append(client_fd)


def update_clients():
    for client in clients:
        buf = server_temple_recv(client)
        if type(buf) == str and buf != '':
            print "fd: " + str(client) + "msg:" + buf
        server_temple_send(client, buf)


def server_temple():
    # define
    server_fd = None
    host = "0.0.0.0"
    port = 7736
    # init
    server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_fd.bind((host, port))
    except Exception as e:
        close(server_fd)
        return

    server_fd.listen(65536)
    server_fd.setblocking(False)
    port = server_fd.getsockname()[1]

    log.debug("success bind port %s" % port)
    log.debug("start success")

    # event loop
    while True:
        time.sleep(0.1)
        accept_client(server_fd)
        update_clients()


if __name__ == '__main__':
    server_temple()
    # s = Server("server", "0.01")
    # s.start()
    # s.run()
