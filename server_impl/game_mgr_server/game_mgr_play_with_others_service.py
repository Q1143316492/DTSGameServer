# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.base.game_mgr import game_mgr


def game_mgr_play_with_others_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_float("matching_time")
    req.check_contain_int("mode")


def game_mgr_play_with_others_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    matching_time = req.content["matching_time"]
    mode = req.content["mode"]

    ret = 0
    err_msg = ''

    if mode == 1:       # 开始匹配
        game_mgr.start_match(user_id, matching_time)
    elif mode == 2:     # 结束匹配, 可能是客户端点的取消
        game_mgr.stop_match(user_id)
        ret = -1
    else:
        ret = -1
        err_msg = "mode not find"

    res.content = {
        "ret": ret,
        "err_msg": err_msg
    }


def game_mgr_play_with_others_service_aftertreatment(controller, req, res):
    pass


class GameMgrPlayWithOthersService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_PLAY_WITH_OTHERS_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_play_with_others_service_run)
        self.func_handler.pre_handler = game_mgr_play_with_others_service_pretreatment
        self.func_handler.last_handler = game_mgr_play_with_others_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE, {
        "user_id": 1,
        "matching_time": 10,
        "mode": 1               # mode == 1 表示开始匹配，到指定matching_time 后自动取消匹配
    })

    TestClient.send(config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE, {
        "user_id": 2,
        "matching_time": 10,
        "mode": 1               # mode == 1 表示开始匹配，到指定matching_time 后自动取消匹配
    })

    TestClient.send(config.GAME_MGR_QUERY_MATCHING_RESULT_SERVICE, {
        "user_id": 1,
        "player_count": 2
    })