# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_core.net_response import Response
from server_impl.server_config import ckv


def game_mgr_aoe_freeze_service_pretreatment(controller, req, res):
    req.check_contain_string("pos")
    req.check_contain_int("room_id")


def game_mgr_aoe_freeze_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_AOE_FREEZE_SERVICE, req.parse_err))
        return

    room_id = req.content["room_id"]
    pos = req.content["pos"]

    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))

    for user_id in room_runtime.user_id_list:
        conn_id = controller.mem_cache.get(ckv.get_ckv_user_to_conn(user_id))
        if not conn_id:
            continue
        r = Response()
        r.conn_id = conn_id
        r.content = {
            "ret": 0,
            "err_msg": '',
            "pos": pos
        }
        res.msg_queue.append(r)

    res.content = {
        "ret": -1,
        "err_msg": ''
    }


def game_mgr_aoe_freeze_service_aftertreatment(controller, req, res):
    pass


class GameMgrAoeFreezeService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_AOE_FREEZE_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_AOE_FREEZE_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_aoe_freeze_service_run)
        self.func_handler.pre_handler = game_mgr_aoe_freeze_service_pretreatment
        self.func_handler.last_handler = game_mgr_aoe_freeze_service_aftertreatment

