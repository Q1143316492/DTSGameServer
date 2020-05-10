# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def game_mgr_query_born_point_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("room_id")


def game_mgr_query_born_point_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_QUERY_BORN_POINT_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    room_id = req.content["room_id"]
    ret = 0
    err_msg = ''
    born_point = -1

    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))

    if room_runtime is None:
        res.content = {
            "ret": -1,
            "err_msg": "room not exist",
            "born": born_point,
            "user_id": user_id
        }
        return

    born_point = room_runtime.fight_system.query_player_born_point(user_id)

    if born_point is None:
        ret = -1
        err_msg = 'user not exist'
        born_point = -1

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "born": born_point,
        "user_id": user_id
    }


def game_mgr_query_born_point_service_aftertreatment(controller, req, res):
    pass


class GameMgrQueryBornPointService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_QUERY_BORN_POINT_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_QUERY_BORN_POINT_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_query_born_point_service_run)
        self.func_handler.pre_handler = game_mgr_query_born_point_service_pretreatment
        self.func_handler.last_handler = game_mgr_query_born_point_service_aftertreatment

