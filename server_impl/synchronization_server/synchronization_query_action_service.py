# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def synchronization_query_action_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")


def synchronization_query_action_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_QUERY_ACTION_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]

    ret = 0
    err_msg = ''
    action = ''

    key = ckv.get_ckv_action_list(user_id)
    action_list = controller.mem_cache.get(key)

    if action_list is None or len(action_list) == 0:
        res.content = {
            "ret": -1,
            "err_msg": "msg empty",
            "action": ""
        }
        return

    if len(action_list) > 10:
        controller.mem_cache.set(key, [])
        ret = -2
        err_msg = "to much message."
    else:
        action = action_list[0]
        action_list = action_list[1:]
        controller.mem_cache.set(key, action_list)

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "action": action
    }


def synchronization_query_action_service_aftertreatment(controller, req, res):
    pass


class SynchronizationQueryActionService:

    def __init__(self):
        if not hasattr(config, "SYNCHRONIZATION_QUERY_ACTION_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.SYNCHRONIZATION_QUERY_ACTION_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, synchronization_query_action_service_run)
        self.func_handler.pre_handler = synchronization_query_action_service_pretreatment
        self.func_handler.last_handler = synchronization_query_action_service_aftertreatment

