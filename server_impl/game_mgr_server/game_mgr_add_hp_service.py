# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def game_mgr_add_hp_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("hp")


def game_mgr_add_hp_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_ADD_HP_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    hp = req.content["hp"]

    # 获取玩家所在房间
    req_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id
    })
    if req_dict["ret"] != 0:
        res.content = {
            "ret": -1,
            "err_msg": '',
        }
        return
    room_id = req_dict["room_id"]
    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))
    room_runtime.fight_system.add_hp(user_id, hp)

    res.content = {
        "ret": 0,
        "err_msg": ''
    }


def game_mgr_add_hp_service_aftertreatment(controller, req, res):
    pass


class GameMgrAddHpService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_ADD_HP_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_ADD_HP_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_add_hp_service_run)
        self.func_handler.pre_handler = game_mgr_add_hp_service_pretreatment
        self.func_handler.last_handler = game_mgr_add_hp_service_aftertreatment

