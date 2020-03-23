from server_core.message import Message
import socket
import errno

fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fd.connect(("localhost", 7736))
fd.setblocking(False)


err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)

recv_buf = ''

msg = Message()
msg.pack_buffer(1001, 'hello!')
fd.sendall(msg.get_stream())

msg.assign()
while True:
    text = ''
    try:
        text = fd.recv(1024)
        if not text:
            err_code = 10000
            fd.close()
            break
    except socket.error, (code, strerror):
        if code not in err_d:
            err_code = code
            fd.close()
            continue
    recv_buf += text

    # message
    while len(recv_buf) != 0:
        size = msg.recv(recv_buf)
        recv_buf = recv_buf[size:]
        if msg.finish():
            print msg.__str__()
            msg.assign()

fd.close()