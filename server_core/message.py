# coding=utf-8
import struct
from server_core import config


class Message:
    """
        消息格式   【4字节消息头，4字节消息句柄，n字节消息内容】
        head 消息头: 4字节 数值表示消息内容的长度
        handler 消息句柄: 4字节 数值表示接口编号，能够通过数值哈希到具体业务函数，该函数能够按序列化协议解析消息内容
        body 消息内容: ...
        todo 包过长判断
    """
    DEFAULT_HEADER_SIZE = 4
    DEFAULT_HANDLER_SIZE = 4

    # 收包状态, 正在收包头，正在收消息句柄，正在收消息内容，收包结束
    PKG_RECV_HEAD = 0
    PKG_RECV_HANDLER = 1
    PKG_RECV_BODY = 2
    PKG_FINISH = 3

    def __init__(self):
        self.__header_size = 4
        self.__handler_size = 4

        self.__header_val = 0
        self.__handler_val = 0
        self.__message_val = ''
        self.__buf = ''
        self.__now_size = 0
        self.__state = Message.PKG_RECV_HEAD

    # 重置消息，进入收包的第一个状态
    def assign(self):
        self.__header_val = 0
        self.__handler_val = 0
        self.__message_val = ''
        self.__buf = ''
        self.__now_size = 0
        self.__state = Message.PKG_RECV_HEAD

    def get_handler(self):
        if self.finish():
            return self.__handler_val
        return None

    def get_msg_content(self):
        if self.finish():
            return self.__message_val
        return None

    # 把当前消息 [包头，句柄，消息体]。转化成网络字节流
    def __pack_buffer(self):
        if not isinstance(self.__header_val, int) or self.__header_val <= 0:
            raise Exception("message header error")
        if not isinstance(self.__handler_val, int):
            raise Exception("message handler error")
        send_buf = struct.pack(">i", self.__header_val)
        send_buf += struct.pack(">i", self.__handler_val)
        send_buf += self.__message_val
        return send_buf

    def get_stream(self):
        return self.__pack_buffer()

    # 直接构造消息
    def pack_buffer(self, handler, buf):
        if not isinstance(handler, int):
            raise Exception("handler must be int")
        self.__header_val = len(buf)
        self.__handler_val = handler
        self.__message_val = buf
        return self.__pack_buffer()

    #    从缓冲区中读取对应字节
    #    @param 缓冲区，缓冲区大小，需要的字节
    def __recv(self, buf, buf_size, need_size):
        read_size = min(buf_size, need_size)
        self.__buf += buf[0: read_size]
        self.__now_size += read_size
        return read_size

    def __reset_buf(self):
        self.__buf = ''
        self.__now_size = 0

    def __str__(self):
        return "[{}][{}][{}]".format(self.__header_val, self.__handler_val, self.__message_val)

    def finish(self):
        return self.__state == Message.PKG_FINISH

    def recv(self, buf):
        buffer_size = len(buf)
        read_size = 0
        if self.__state == Message.PKG_RECV_HEAD:
            read_size = self.__recv(buf, buffer_size, self.__header_size - self.__now_size)
            if self.__now_size == self.__header_size:
                self.__state = Message.PKG_RECV_HANDLER
                self.__header_val = struct.unpack(">i", self.__buf)[0]
                # todo 消息长度不合法重置消息, 这里或许应该杀死客户端
                if self.__header_val <= 0 or self.__header_val > config.MAX_MESSAGE_SIZE:
                    self.assign()

                self.__reset_buf()
        elif self.__state == Message.PKG_RECV_HANDLER:
            read_size = self.__recv(buf, buffer_size, self.__handler_size - self.__now_size)
            if self.__now_size == self.__handler_size:
                self.__state = Message.PKG_RECV_BODY
                self.__handler_val = struct.unpack(">i", self.__buf)[0]
                self.__reset_buf()
        elif self.__state == Message.PKG_RECV_BODY:
            read_size = self.__recv(buf, buffer_size, self.__header_val - self.__now_size)
            if self.__now_size == self.__header_val:
                self.__state = Message.PKG_FINISH
                self.__message_val = self.__buf
                self.__reset_buf()
        return read_size
