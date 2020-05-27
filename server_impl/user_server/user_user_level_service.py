# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.base.orm.user_level import UserLevel
from server_impl.server_config import ckv


def user_user_level_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("opt")
    req.check_contain_int("val")


def user_user_level_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.USER_USER_LEVEL_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    opt = req.content["opt"]
    val = req.content["val"]

    user_level = UserLevel.select_user_level_by_user_id(user_id)
    exist = True
    if user_level is None:
        exist = False
        user_level = UserLevel()
        user_level.user_id = user_id
        user_level.level = 0

    if opt == 1:    # 上报
        user_level.level += val
        if not exist:
            user_level.insert_to_db()
        else:
            user_level.update_user_level_by_user_id()
        res.content = {
            "ret": 0,
            "opt": opt,
            "err_msg": ''
        }
        return

    if opt == 2:
        if not exist:
            user_level.insert_to_db()
        res.content = {
            "ret": 0,
            "err_msg": '',
            "opt": opt,
            "val": user_level.level
        }
        return

    res.content = {
        "ret": -1
    }


def user_user_level_service_aftertreatment(controller, req, res):
    pass


class UserUserLevelService:

    def __init__(self):
        if not hasattr(config, "USER_USER_LEVEL_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.USER_USER_LEVEL_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, user_user_level_service_run)
        self.func_handler.pre_handler = user_user_level_service_pretreatment
        self.func_handler.last_handler = user_user_level_service_aftertreatment

