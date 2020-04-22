# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv

"""
    查询一个玩家所在的房间号
"""


def room_mgr_query_user_belonged_room_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")


def room_mgr_query_user_belonged_room_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE, req.parse_err))
        return

    user_id = str(req.content["user_id"])

    ret = 0
    err_msg = ""

    query_ret = controller.mem_cache.get(ckv.get_ckv_user_enter_room(user_id))
    room_type, room_id = -1, -1
    if query_ret is not None:
        room_type, room_id = query_ret.split("#")
    else:
        ret = -1
        err_msg = "room_query_user_belonged_room_service user not exist "

    # 设置返回 dict
    res.content = {
        "ret": ret,
        "room_type": room_type,
        "room_id": room_id,
        "err_msg": err_msg
    }


def room_mgr_query_user_belonged_room_service_aftertreatment(controller, req, res):
    pass


class RoomMgrQueryUserBelongedRoomService:

    def __init__(self):
        if not hasattr(config, "ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_mgr_query_user_belonged_room_service_run)
        self.func_handler.pre_handler = room_mgr_query_user_belonged_room_service_pretreatment
        self.func_handler.last_handler = room_mgr_query_user_belonged_room_service_aftertreatment


if __name__ == '__main__':
    pass
    from server_impl.test_client import TestClient

    TestClient.send(config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE, {
        "user_id": 2
    })