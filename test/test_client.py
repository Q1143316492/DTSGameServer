# coding=utf-8
import json

from server_core.message import Message
from server_core.net_request import Request
from server_core import config
import socket
import errno



def test_server(handler, content):
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # fd.connect(("117.78.5.122", 7736))
    fd.connect(("127.0.0.1", 7736))
    fd.setblocking(False)

    err_d = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)

    recv_buf = ''

    msg = Message()
    # content = {
    #     "user_id": 23,
    #     "sub_server_id": 1,
    #     "room_type": 1
    # }
    req = Request()
    req.pack_buffer(handler, content)

    fd.sendall(req.msg.get_stream())

    msg.assign()

    ok = False

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
                ok = True

        if ok:
            break

    fd.close()


if __name__ == '__main__':
    # 测试加入房间
    # test_server(config.ROOM_ENTER_ROOM_SERVICE, {
    #     "user_id": 1,
    #     "sub_server_id": 1,
    #     "room_type": 1
    # })
    # test_server(config.ROOM_ENTER_ROOM_SERVICE, {
    #     "user_id": 22,
    #     "sub_server_id": 1,
    #     "room_type": 1
    # })
    # test_server(config.ROOM_ENTER_ROOM_SERVICE, {
    #     "user_id": 44,
    #     "sub_server_id": 1,
    #     "room_type": 1
    # })
    # test_server(config.ROOM_QUERY_ROOM_USERS_SERVICE, {
    #     "room_id": 1
    # })

    # test_server(config.SYNCHRONIZATION_REPORT_TRANSFORM_SERVICE, {
    #     "user_id": 1,
    #     "position": "0;0;0",
    #     "rotation": "0;0;0"
    # })
    # test_server(config.SYNCHRONIZATION_QUERY_USER_TRANSFORM_SERVICE, {
    #     "user_id": 1
    # })

    test_server(config.USER_LOGIN_SERVICE, {
        "username": "netease1",
        "password": "123456"
    })