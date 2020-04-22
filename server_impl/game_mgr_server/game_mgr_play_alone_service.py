# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config


def game_mgr_play_alone_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")


def game_mgr_play_alone_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_PLAY_ALONE_SERVICE, req.parse_err))
        return

    user_id = str(req.content["user_id"])
    ret = 0
    err_msg = ''

    res_dict = controller.handler_dict[config.ROOM_MGR_ENTER_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id,
        "room_type": 2
    })

    if res_dict["ret"] != 0:
        ret = res_dict["ret"]
        err_msg = "ROOM_MGR_ENTER_ROOM_SERVICE error: " + res_dict["err_msg"]

    res.content = {
        "ret": ret,
        "err_msg": err_msg
    }


def game_mgr_play_alone_service_aftertreatment(controller, req, res):
    pass


class GameMgrPlayAloneService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_PLAY_ALONE_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_PLAY_ALONE_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_play_alone_service_run)
        self.func_handler.pre_handler = game_mgr_play_alone_service_pretreatment
        self.func_handler.last_handler = game_mgr_play_alone_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.GAME_MGR_PLAY_ALONE_SERVICE, {
        "user_id": 1
    })