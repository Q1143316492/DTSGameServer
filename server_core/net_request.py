# coding=utf-8
from server_core.message import Message
from server_core.log import Log
import copy
import json


def unicode_convert(item):
    if isinstance(item, dict):
        return { unicode_convert(key): unicode_convert(value) for key, value in item.iteritems() }
    elif isinstance(item, list):
        return [ unicode_convert(element) for element in item ]
    elif isinstance(item, unicode):
        return item.encode('utf-8')
    else:
        return item


class Request:

    def __init__(self, conn_id, msg=None):
        if msg is None:
            self.msg = Message()
        else:
            self.msg = copy.copy(msg)
        self.conn_id = conn_id
        self.content = None
        self.logger = Log()
        self.parse_success = False

    def get_handler(self):
        return self.msg.get_handler()

    def get_msg_content(self):
        return self.msg.get_msg_content()

    def deserialization(self):
        try:
            self.content = json.loads(self.msg.get_msg_content())
        except ValueError as err:
            self.logger.debug("json parse err. " + str(err))
            return
        self.parse_success = True
