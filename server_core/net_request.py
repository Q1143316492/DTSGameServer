# coding=utf-8
from server_core.message import Message
from server_core.log import Log
import copy
import json


def unicode_convert(item):
    if isinstance(item, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in item.iteritems()}
    elif isinstance(item, list):
        return [unicode_convert(element) for element in item]
    elif isinstance(item, unicode):
        return item.encode('utf-8')
    else:
        return item


class Request:

    def __init__(self, conn_id=0, msg=None):
        if msg is None:
            self.msg = Message()
        else:
            self.msg = copy.copy(msg)
        self.conn_id = conn_id
        self.content = None
        self.logger = Log()
        self.parse_success = False
        self.parse_err = None

    def get_handler(self):
        return self.msg.get_handler()

    def get_msg_content(self):
        return self.msg.get_msg_content()

    def pack_buffer(self, handler, content=None):
        if content and isinstance(content, dict):
            self.content = content
        if not isinstance(self.content, dict):
            raise ValueError("request/response content must be dict")
        self.content = unicode_convert(self.content)
        self.msg.pack_buffer(handler, json.dumps(self.content))

    def deserialization(self):
        try:
            self.content = json.loads(self.msg.get_msg_content())
        except ValueError as err:
            self.logger.debug("json parse err. " + str(err))
            return
        self.content = unicode_convert(self.content)
        self.parse_success = True

    def contain_key(self, key):
        if key not in self.content.keys():
            self.parse_success = False
            self.parse_err = "key not exist. " + key
            return False
        return True

    def check_contain_string(self, key):
        if not self.contain_key(key):
            return False
        if not isinstance(self.content[key], str):
            self.parse_success = False
            self.parse_err = "key: " + key + " is not str"
            return False
        return True

    def check_contain_int(self, key, min_val=None, max_val=None):
        if not self.contain_key(key):
            return False
        val = self.content[key]
        if not isinstance(val, int):
            self.parse_success = False
            self.parse_err = "key: " + key + "is not int"
            return False
        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            self.parse_success = False
            self.parse_err = "key: " + key + " value range error"
            return False
        return True

# json 备注
# str = json.dumps(obj)
# obj = json.loads(str) ValueError
