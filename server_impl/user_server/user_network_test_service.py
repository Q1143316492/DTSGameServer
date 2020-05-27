# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config


def user_network_test_service_pretreatment(controller, req, res):
    req.check_contain_int("last_time")
    req.check_contain_string("msg")


def user_network_test_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.USER_NETWORK_TEST_SERVICE, req.parse_err))
        return

    last_time = req.content["last_time"]
    msg = req.content["msg"]

    res.content = {
        "ret": 0,
        "err_msg": '',
        "last_time": last_time,
        "extend": msg,
    }


def user_network_test_service_aftertreatment(controller, req, res):
    pass


class UserNetworkTestService:

    def __init__(self):
        if not hasattr(config, "USER_NETWORK_TEST_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_NETWORK_TEST_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, user_network_test_service_run)
        self.func_handler.pre_handler = user_network_test_service_pretreatment
        self.func_handler.last_handler = user_network_test_service_aftertreatment

