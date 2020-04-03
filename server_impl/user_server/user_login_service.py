# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
import json


def user_login_service_pretreatment(controller, req, res):
    req.check_contain_string("username")
    req.check_contain_string("password")


def user_login_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.USER_LOGIN_SERVICE, req.parse_err))
        return

    Log().debug("login service: " + str(req.msg))

    # 获取参数
    username = req.content["username"]
    password = req.content["password"]
    # 处理业务
    login_success = False

    user_list = {
        "netease1": "123456",
        "netease2": "123456",
        "netease3": "123456",
    }
    if username in user_list and password == user_list[username]:
        login_success = True

    # 设置返回 dict
    res.content = {
        "ret": 0,
        "login_success": login_success
    }


def user_login_service_aftertreatment(controller, req, res):
    pass


class UserLoginService:

    def __init__(self):
        if not hasattr(config, "USER_LOGIN_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_LOGIN_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, user_login_service_run)
        self.func_handler.pre_handler = user_login_service_pretreatment
        self.func_handler.last_handler = user_login_service_aftertreatment
