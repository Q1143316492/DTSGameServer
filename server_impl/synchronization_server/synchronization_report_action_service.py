# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def synchronization_report_action_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_string("action")


def synchronization_report_action_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_REPORT_ACTION_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    action = req.content["action"]

    key = ckv.get_ckv_action_list(user_id)
    action_list = controller.mem_cache.get(key)
    if action_list is None:
        action_list = []
    action_list.append(action)
    controller.mem_cache.set(key, action_list)

    res.content = {
        "ret": 0,
        "err_msg": ''
    }


def synchronization_report_action_service_aftertreatment(controller, req, res):
    pass


class SynchronizationReportActionService:

    def __init__(self):
        if not hasattr(config, "SYNCHRONIZATION_REPORT_ACTION_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.SYNCHRONIZATION_REPORT_ACTION_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, synchronization_report_action_service_run)
        self.func_handler.pre_handler = synchronization_report_action_service_pretreatment
        self.func_handler.last_handler = synchronization_report_action_service_aftertreatment

