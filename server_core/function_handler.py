# coding=utf-8
from server_core.log import Log


class FunctionHandler:

    def __init__(self, handler_id, handler):
        self.handler_id = handler_id
        self.pre_handler = None
        self.handler = handler
        self.last_handler = None

        if not isinstance(self.handler_id, int) or not callable(handler):
            raise Exception("function handler style error")

        self.logger = Log()

    def set_pre_handler(self, handler):
        if callable(handler):
            self.pre_handler = handler

    def set_last_handler(self, handler):
        if callable(handler):
            self.last_handler = handler

    def run(self, req, res):
        try:
            self.system_pretreatment(req, res)
            if callable(self.pre_handler):
                self.pre_handler(req, res)
            self.handler(req, res)
            if callable(self.last_handler):
                self.last_handler(req, res)
            self.system_aftertreatment(req, res)
        except Exception as e:
            logger = Log()
            logger.error("[function_handler] service error. handler " + str(req.msg.get_handler()))
            logger.error("req.msg: " + str(req.msg))
            logger.error("err: " + e.message)

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
