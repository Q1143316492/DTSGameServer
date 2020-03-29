# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config


class UserLoginService:

    def __init__(self):
        if not hasattr(config, "USER_LOGIN_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_LOGIN_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, UserLoginService.user_login_service_run)
        self.func_handler.pre_handler = UserLoginService.user_login_service_pretreatment
        self.func_handler.last_handler = UserLoginService.user_login_service_aftertreatment

    @staticmethod
    def user_login_service_pretreatment(req, res):
        req.deserialization()

    @staticmethod
    def user_login_service_run(req, res):
        Log().info(req.msg)
        Log().info("login:test")
        res.msg = req.msg

    @staticmethod
    def user_login_service_aftertreatment(req, res):
        pass