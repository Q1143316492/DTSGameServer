# coding=utf-8
import struct
import binascii
import socket
import sys
from server_core.message import Message


def test_header():
    val = 16
    big_ending = struct.pack(">I", val)
    print type(big_ending), len(big_ending)  # str, 4
    print binascii.hexlify(big_ending)  # 字符串的十六进制表示


def test_pack():
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect(("localhost", 7736))

    msg = Message()
    msg.pack_buffer(1001, "hello world")
    str = msg.get_stream()
    fd.sendall(str)


if __name__ == '__main__':
    msg1 = Message()
    msg1.pack_buffer(1001, 'hello world')
    stream1 = msg1.get_stream()

    msg2 = Message()
    msg2.pack_buffer(1002, 'bye world')
    stream2 = msg2.get_stream()

    print stream1, stream2

    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.connect(("localhost", 7736))

    # 测试粘包
    stream = stream1 + stream2
    fd.sendall(stream)

    # 测试缺包
    fd.sendall(stream1[:4])
    fd.sendall(stream1[4:])
    fd.sendall(stream2[:5])
    fd.sendall(stream2[5:])
