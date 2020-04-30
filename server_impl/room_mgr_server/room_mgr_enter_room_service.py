# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.base.sync_mgr import frame_sync
from server_impl.server_config import ckv
from server_impl.base.room_mgr import game_room, room_mgr
from server_impl.base.game_mgr import game_mgr
from server_impl.base.user_mgr import user_mgr


"""
    玩家进入某个房间
    room_type 表示房间号
        room_type == 1 的时候是游戏大厅。游戏开始所有玩家都进入的一个场景
        room_type == ? 其他值，每一个值代表一个地图。需要申请一个递增的房间号。把玩家从原来房间退出。丢到新场景
        
    会设置几个 key val 值
        user_id : room_type#room_id
        room_id : 这个房间的玩家列表
"""


def room_mgr_enter_room_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("room_type")


def room_mgr_enter_room_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_MGR_ENTER_ROOM_SERVICE, req.parse_err))
        return

    user_id = str(req.content["user_id"])
    room_type = req.content["room_type"]

    ret = 0
    room_id = 0
    err_msg = ""

    if room_type == 1:  # 预设 room_type == 1 表示玩家申请加入游戏大厅
        room_id = 0
    elif room_type == 2:    # 预设 room_type == 2 表示玩家主动申请新房间
        res_dict = controller.handler_dict[config.ROOM_MGR_REGISTER_A_ROOM_SERVICE].inline_call(controller, {
            "user_id": user_id
        })
        if res_dict["ret"] == 0:
            room_id = res_dict["room_id"]
        else:
            ret = res_dict["ret"]
            err_msg = "register room fail. " + res_dict["err_msg"]
    elif room_type == 3:   # 预设 room_type == 3 表示玩家加入某个指定房间，中途加入，或者多个玩家匹配加入
        if "room_id" not in req.content.keys():
            res.content = {
                "ret": -1,
                "room_id": -1,
                "err_msg": "room_id not found"
            }
            return
        else:
            room_id = req.content["room_id"]
    else:
        res.content = {
            "ret": -1,
            "room_id": -1,
            "err_msg": "room_type un define"
        }
        return

    game_room.out_of_last_room(controller, user_id)

    user_runtime = game_mgr.init_user_runtime(controller, user_id)
    user_runtime.set_room(room_type=room_type, room_id=room_id)
    user_runtime.restart()

    room_runtime = game_mgr.init_room_runtime(controller, room_id)
    if not room_runtime.add_user(user_id):
        ret = -1
        err_msg = "user has already in room"
        room_id = -1

    res.content = {
        "ret": ret,
        "room_id": room_id,
        "err_msg": err_msg
    }


def room_mgr_enter_room_service_aftertreatment(controller, req, res):
    pass


class RoomMgrEnterRoomService:

    def __init__(self):
        if not hasattr(config, "ROOM_MGR_ENTER_ROOM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_MGR_ENTER_ROOM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_mgr_enter_room_service_run)
        self.func_handler.pre_handler = room_mgr_enter_room_service_pretreatment
        self.func_handler.last_handler = room_mgr_enter_room_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.ROOM_MGR_ENTER_ROOM_SERVICE, {
        "user_id": 1,
        "room_type": 2,
    })

    TestClient.send(config.ROOM_MGR_ENTER_ROOM_SERVICE, {
        "user_id": 1,
        "room_type": 2,
    })
    # TestClient.send(config.ROOM_MGR_EXIST_ROOM_SERVICE, {
    #     "user_id": "1"
    # })

    # TestClient.send(config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE, {
    #     "user_id": 1
    # })
    #
    # TestClient.send(config.ROOM_MGR_QUERY_ROOM_USERS_SERVICE, {
    #     "room_id": 1
    # })
