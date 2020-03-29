# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config


class UserRegisterService:

    def __init__(self):
        if not hasattr(config, "USER_REGISTER_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_REGISTER_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, UserRegisterService.user_register_service_run)
        self.func_handler.pre_handler = UserRegisterService.user_register_service_pretreatment
        self.func_handler.last_handler = UserRegisterService.user_register_service_aftertreatment

    @staticmethod
    def user_register_service_pretreatment(req, res):
        pass

    @staticmethod
    def user_register_service_run(req, res):
        pass

    @staticmethod
    def user_register_service_aftertreatment(req, res):
        pass