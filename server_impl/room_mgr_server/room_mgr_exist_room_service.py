# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
from server_impl.base.room_mgr import game_room
from server_impl.base.sync_mgr import sync_mgr

"""
    玩家退出某个房间，进入一种不属于所有房间的过度状态
    
"""


def room_mgr_exist_room_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")


def room_mgr_exist_room_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_MGR_EXIST_ROOM_SERVICE, req.parse_err))
        return

    user_id = str(req.content["user_id"])

    # 查询这个玩家之前在那个房间, 然后删除记录
    game_room.out_of_last_room(controller, res, user_id)

    # 清除玩家上报的同步信息
    sync_mgr.clear_sync_msg(controller, user_id)

    res.content = {
        "ret": 0,
        "err_msg": '',
    }


def room_mgr_exist_room_service_aftertreatment(controller, req, res):
    pass


class RoomMgrExistRoomService:

    def __init__(self):
        if not hasattr(config, "ROOM_MGR_EXIST_ROOM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_MGR_EXIST_ROOM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_mgr_exist_room_service_run)
        self.func_handler.pre_handler = room_mgr_exist_room_service_pretreatment
        self.func_handler.last_handler = room_mgr_exist_room_service_aftertreatment


if __name__ == '__main__':
    pass