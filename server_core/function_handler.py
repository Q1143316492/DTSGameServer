# coding=utf-8
from server_core.log import Log
from server_core.net_request import Request
from server_core.net_response import Response
from server_core import config
import time
import copy


class FunctionHandler:

    def __init__(self, handler_id, handler):
        self.handler_id = handler_id
        self.pre_handler = None
        self.handler = copy.copy(handler)
        self.last_handler = None

        if not isinstance(self.handler_id, int) or not callable(handler):
            raise Exception("function handler style error")

        self.logger = Log()

    def set_pre_handler(self, handler):
        if callable(handler):
            self.pre_handler = copy.copy(handler)

    def set_last_handler(self, handler):
        if callable(handler):
            self.last_handler = copy.copy(handler)

    def call(self, controller, req, res):
        req.msg.un_encryption()
        self.system_pretreatment(req, res)  # 字符流的 req.msg，变成 python dict 存在于 req.content
        if callable(self.pre_handler):
            self.pre_handler(controller, req, res)
        self.handler(controller, req, res)
        if callable(self.last_handler):
            self.last_handler(controller, req, res)
        self.system_aftertreatment(req, res)
        res.msg.encryption()

    def run(self, controller, req, res):
        is_debug = config.ConfigLoader().get("debug")
        if isinstance(is_debug, bool) and is_debug:
            self.call(controller, req, res)
        else:
            try:
                self.call(controller, req, res)
            except Exception as e:
                logger = Log()
                logger.error("[function_handler] service error. handler " + str(req.msg.get_handler())
                             + "\nreq.msg: " + str(req.msg)
                             + "err: " + e.message)

    def inline_call_prepare(self, controller, req_dict):
        req = Request()
        req.content = req_dict
        req.parse_success = True  # 内部调用 service，跳过了解析那一步，所以手动设置解析成功
        res = Response()
        if callable(self.pre_handler):
            self.pre_handler(controller, req, res)
        self.handler(controller, req, res)
        if callable(self.last_handler):
            self.last_handler(controller, req, res)
        return res.content

    def inline_call(self, controller, req_dict):
        is_debug = config.ConfigLoader().get("debug")
        if isinstance(is_debug, bool) and is_debug:
            return self.inline_call_prepare(controller, req_dict)

        try:
            return self.inline_call_prepare(controller, req_dict)
        except Exception as e:
            logger = Log()
            logger.error("[function_handler inline call] service error. handler " + str(self.handler_id)
                         + "req.msg: " + str(req_dict)
                         + "err: " + e.message)
            return None

    @staticmethod
    def system_pretreatment(req, res):
        req.deserialization()

    @staticmethod
    def system_aftertreatment(req, res):
        try:
            res.pack_buffer(req.msg.get_handler())
        except Exception as e:
            Log().warn("system_aftertreatment err. " + str(e) + " req " + str(req.msg))

        if not res.msg.finish():
            res.msg.pack_buffer(0, "err")
            return
