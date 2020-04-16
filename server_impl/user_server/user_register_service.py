# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
import multiprocessing
import json


def user_register_service_pretreatment(controller, req, res):
    req.check_contain_string("username")
    req.check_contain_string("password")


def user_register_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err" % config.USER_LOGIN_SERVICE)
        return

    Log().debug("register service: " + str(req.msg))

    # 获取参数
    username = req.content["username"]
    password = req.content["password"]

    # 处理业务 TODO
    print "register_call"

    # 设置返回 dict
    res.content = {
        "ret": 0,
        "register_success": False
    }


def user_register_service_aftertreatment(controller, req, res):
    pass


class UserRegisterService:

    def __init__(self):
        if not hasattr(config, "USER_REGISTER_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_REGISTER_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, user_register_service_run)
        self.func_handler.pre_handler = user_register_service_pretreatment
        self.func_handler.last_handler = user_register_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient
    TestClient.send(config.USER_REGISTER_SERVICE, {
        "username": "cwl",
        "password": "123"
    })