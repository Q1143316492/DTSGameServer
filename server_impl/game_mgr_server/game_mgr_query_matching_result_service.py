# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
from server_impl.base.game_mgr import game_mgr
from server_impl.base.room_mgr import game_room


def game_mgr_query_matching_result_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("player_count")


def game_mgr_query_matching_result_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_QUERY_MATCHING_RESULT_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    player_count = req.content["player_count"]

    ret = 0
    err_msg = ''

    key = ckv.get_ckv_user_in_matching()
    matching_list = controller.mem_cache.get(key)
    room_id = 0

    # 说明这个玩家已经匹配成功
    if user_id not in matching_list:
        res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
            "user_id": user_id,
        })
        if res_dict['ret'] != 0:
            game_mgr.stop_match(user_id)
            ret = -2
            err_msg = "user not match. " + res_dict['err_msg']
        else:
            room_id = res_dict['room_id']
    else:
        if len(matching_list) >= player_count:
            room_id, ret, err_msg = game_room.register_a_room(controller, user_id)
            if ret != 0:
                res.content = {
                    "ret": ret,
                    "err_msg": err_msg,
                    "room_id": room_id
                }
                return

            # 把目前所有玩家丢到匹配房间
            num, ret, err_msg = game_mgr.matching_some_players(controller, matching_list, room_id)
            matching_list = matching_list[num:]
            controller.mem_cache.set(key, matching_list)

        else:
            ret = -1
            err_msg = "not enough players"

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "room_id": room_id
    }


def game_mgr_query_matching_result_service_aftertreatment(controller, req, res):
    pass


class GameMgrQueryMatchingResultService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_QUERY_MATCHING_RESULT_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_QUERY_MATCHING_RESULT_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_query_matching_result_service_run)
        self.func_handler.pre_handler = game_mgr_query_matching_result_service_pretreatment
        self.func_handler.last_handler = game_mgr_query_matching_result_service_aftertreatment

