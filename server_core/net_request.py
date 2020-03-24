# coding=utf-8
from server_core.message import Message
import copy

class Request:

    def __init__(self, conn_id, msg=None):
        if msg is None:
            self.msg = Message()
        else:
            self.msg = copy.copy(msg)
        self.conn_id = conn_id

    def get_handler(self):
        return self.msg.get_handler()

    def get_msg_content(self):
        return self.msg.get_msg_content()
