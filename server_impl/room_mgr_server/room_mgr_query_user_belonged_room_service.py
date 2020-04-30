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

    room_type = -1
    room_id = -1

    user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))

    if user_runtime is None:
        ret = -1
        err_msg = 'user not enter any room'
    else:
        room_type, room_id = user_runtime.get_room()

        if room_type is None or room_id is None:
            ret = -1
            err_msg = 'room not exist'

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