# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def synchronization_report_transform_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_string("position")
    req.check_contain_string("rotation")
    req.check_contain_int("time")


def synchronization_report_transform_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_REPORT_TRANSFORM_SERVICE, req.parse_err))
        return

    user_id = str(req.content["user_id"])
    position = req.content["position"]
    rotation = req.content["rotation"]
    req_time = req.content["time"]

    user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))
    user_runtime.role.set_transform(position=position, rotation=rotation)

    # 设置返回 dict
    res.content = {
        "ret": 0,
        "err_msg": "",
        "time": req_time
    }


def synchronization_report_transform_service_aftertreatment(controller, req, res):
    pass


class SynchronizationReportTransformService:

    def __init__(self):
        if not hasattr(config, "SYNCHRONIZATION_REPORT_TRANSFORM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.SYNCHRONIZATION_REPORT_TRANSFORM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, synchronization_report_transform_service_run)
        self.func_handler.pre_handler = synchronization_report_transform_service_pretreatment
        self.func_handler.last_handler = synchronization_report_transform_service_aftertreatment

