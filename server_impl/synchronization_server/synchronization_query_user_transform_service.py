# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
import json


def synchronization_query_user_transform_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("time")


def synchronization_query_user_transform_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_QUERY_USER_TRANSFORM_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    req_time = req.content["time"]
    err_msg = ""
    ret = 0

    # 处理业务

    user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))
    position, rotation = user_runtime.role.get_transform()

    if position is None or rotation is None:
        ret = -1
        err_msg = "key not exist"
        position = ''
        rotation = ''

    res.content = {
        "ret": ret,
        "user_id": user_id,
        "position": position,
        "rotation": rotation,
        "err_msg": err_msg,
        "time": req_time
    }


def synchronization_query_user_transform_service_aftertreatment(controller, req, res):
    pass


class SynchronizationQueryUserTransformService:

    def __init__(self):
        if not hasattr(config, "SYNCHRONIZATION_QUERY_USER_TRANSFORM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.SYNCHRONIZATION_QUERY_USER_TRANSFORM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, synchronization_query_user_transform_service_run)
        self.func_handler.pre_handler = synchronization_query_user_transform_service_pretreatment
        self.func_handler.last_handler = synchronization_query_user_transform_service_aftertreatment

