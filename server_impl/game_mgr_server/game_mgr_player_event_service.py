# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def game_mgr_player_event_service_pretreatment(controller, req, res):
    req.check_contain_int("room_id")
    req.check_contain_int("opt")
    req.check_contain_int("event")
    req.check_contain_string("param")


def game_mgr_player_event_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_PLAYER_EVENT_SERVICE, req.parse_err))
        return

    room_id = req.content["room_id"]
    opt = req.content["opt"]
    event = req.content["event"]
    param = req.content["param"]

    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))

    res.content = {
        "ret": 0,
        "opt": opt,
        "err_msg": ''
    }


def game_mgr_player_event_service_aftertreatment(controller, req, res):
    pass


class GameMgrPlayerEventService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_PLAYER_EVENT_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_PLAYER_EVENT_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_player_event_service_run)
        self.func_handler.pre_handler = game_mgr_player_event_service_pretreatment
        self.func_handler.last_handler = game_mgr_player_event_service_aftertreatment

