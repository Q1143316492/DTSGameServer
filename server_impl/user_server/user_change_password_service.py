# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.base.orm.user import User
from server_impl.base.common import common


def user_change_password_service_pretreatment(controller, req, res):
    req.check_contain_string("username")
    req.check_contain_string("password")
    req.check_contain_string("old_password")


def user_change_password_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.USER_CHANGE_PASSWORD_SERVICE, req.parse_err))
        return

    username = req.content["username"]
    password = req.content["password"]
    old_password = req.content["old_password"]

    print username, password, old_password

    ret = 0
    success = False
    err_msg = ''

    user = User.select_user_by_user_name(username)

    if user is None:
        success = False
        err_msg = 'user not exist'
        res.content = {
            "ret": 0,
            "success": success,
            "err_msg": err_msg
        }
        return

    if user.md5_str == common.get_md5_str(old_password + user.salt):
        user.password = password
        user.update_user_by_user_id()
        success = True
    else:
        err_msg = 'old password not right'
        success = False

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "success": success
    }


def user_change_password_service_aftertreatment(controller, req, res):
    pass


class UserChangePasswordService:

    def __init__(self):
        if not hasattr(config, "USER_CHANGE_PASSWORD_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_CHANGE_PASSWORD_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, user_change_password_service_run)
        self.func_handler.pre_handler = user_change_password_service_pretreatment
        self.func_handler.last_handler = user_change_password_service_aftertreatment

