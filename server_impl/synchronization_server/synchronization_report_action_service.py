# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
from server_impl.base.sync_mgr import frame_sync


def synchronization_report_action_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_string("action")
    req.check_contain_int("frame")


def synchronization_report_action_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_REPORT_ACTION_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    action = req.content["action"]
    client_frame = req.content["frame"]

    err_msg = ''

    # 查询用户所在游戏房间
    req_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id
    })
    if req_dict["ret"] != 0:
        res.content = {
            "ret": -1,
            "err_msg": "report action error:" + req_dict["err_msg"]
        }
        return
    room_id = req_dict["room_id"]

    # 同步
    # TODO REPORT
    key = ckv.get_ckv_action_list(room_id)
    sync_controller = controller.mem_cache.get(key)

    if sync_controller is None:
        sync_controller = frame_sync.FrameSync(room_id)
        controller.mem_cache.set(ckv.get_ckv_action_list(room_id), sync_controller)

    if sync_controller.report_logic_frame(controller, client_frame, user_id, action):
        ret = 0
    else:
        ret = -1

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "frame": sync_controller.server_frame
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
