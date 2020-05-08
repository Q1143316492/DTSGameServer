# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def game_mgr_fight_system_service_pretreatment(controller, req, res):
    req.check_contain_int("room_id")
    req.check_contain_string("opt")
    req.check_contain_string("param")


def game_mgr_fight_system_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_FIGHT_SYSTEM_SERVICE, req.parse_err))
        return

    room_id = req.content["room_id"]
    opt = req.content["opt"]
    param = req.content["param"]    # 客户端上来的参数按 英文逗号分隔

    msg = ''

    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))

    if room_runtime is None:
        res.content = {
            "ret": -1,
            "err_msg": '',
            "opt": opt,
            "msg": msg
        }
        return

    if opt == "attacked":
        player_id, hp = [int(v) for v in param.split(",")]
        room_runtime.fight_system.attacked(player_id, hp)
    elif opt == "query_players":
        msg = room_runtime.fight_system.query_players_hp()

    res.content = {
        "ret": 0,
        "err_msg": '',
        "opt": opt,
        "msg": msg
    }


def game_mgr_fight_system_service_aftertreatment(controller, req, res):
    pass


class GameMgrFightSystemService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_FIGHT_SYSTEM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_FIGHT_SYSTEM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_fight_system_service_run)
        self.func_handler.pre_handler = game_mgr_fight_system_service_pretreatment
        self.func_handler.last_handler = game_mgr_fight_system_service_aftertreatment


if __name__ == '__main__':
    a = [1, 2]
    c, d = a
    print c, d