# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.base.orm.user import User
from server_impl.base.common import common


def user_login_service_pretreatment(controller, req, res):
    req.check_contain_string("username")
    req.check_contain_string("password")
    req.check_contain_int("time")


def user_login_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.USER_LOGIN_SERVICE, req.parse_err))
        return

    username = req.content["username"]
    password = req.content["password"]
    req_time = req.content["time"]
    login_success = False

    user = User.select_user_by_user_name(username)

    if user is None:
        res.content = {
            "ret": -1,
            "login_success": login_success,
            "user_id": -1,
            "time": req_time
        }
        return

    res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user.user_id,
    })
    if res_dict["ret"] == 0:
        res.content = {
            "ret": -1,
            "login_success": False,
            "user_id": -1,
            "time": req_time
        }
        return

    if user.md5_str == common.get_md5_str(password + user.salt):
        login_success = True
    else:
        login_success = False

    res.content = {
        "ret": 0,
        "login_success": login_success,
        "user_id": user.user_id,
        "time": req_time
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


if __name__ == '__main__':
    pass

    from server_impl.test_client import TestClient

    # TestClient.send(config.USER_LOGIN_SERVICE, {
    #     "username": "netease1",
    #     "password": "123456",
    #     "time": 5
    # })
    #
    # TestClient.send(config.USER_LOGIN_SERVICE, {
    #     "username": "netease33",
    #     "password": "123456",
    #     "time": 5
    # })
