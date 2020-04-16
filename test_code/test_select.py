# coding=utf-8
import errno
import socket
import time
import select
import Queue

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


def close(fd):
    try:
        fd.close()
    except Exception as e:
        log.error("test_code socket close fail err:" + e.message)


def server_temple():
    # define
    server_fd = None
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

    server_fd.listen(65536)
    server_fd.setblocking(False)
    port = server_fd.getsockname()[1]

    log.debug("success bind port %s" % port)
    log.debug("start success")

    inputs = [server_fd]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        # handle read
        for s in readable:
            if s is server_fd:
                # try
                client_fd, remote = s.accept()
                client_fd.setblocking(False)
                inputs.append(client_fd)
                message_queues[client_fd] = Queue.Queue()
                print 'accept'
            else:
                # try
                data = s.recv(1024)
                print type(s)
                if data:
                    print 'recv data' + data
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    print 'client out'
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        # handle write
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                outputs.remove(s)
            else:
                print "send msg:" + next_msg
                s.sendall(next_msg)

        # handle exception
        for s in exceptional:
            print "exception" + str(s)
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == '__main__':
    server_temple()
    # s = Server("server", "0.01")
    # s.start()
    # s.run()

