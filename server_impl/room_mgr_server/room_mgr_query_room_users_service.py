# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
import json


def room_mgr_query_room_users_service_pretreatment(controller, req, res):
    req.check_contain_int("room_id")


def room_mgr_query_room_users_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_MGR_QUERY_ROOM_USERS_SERVICE, req.parse_err))
        return

    room_id = req.content["room_id"]
    err_msg = ""
    ret = 0

    key = ckv.get_ckv_query_room_users(room_id)
    user_id_list = controller.mem_cache.get(key)

    if user_id_list is None:
        ret = -1
        err_msg = "room id not exist"

    res.content = {
        "ret": ret,
        "user_id_list": user_id_list,
        "err_msg": err_msg
    }


def room_mgr_query_room_users_service_aftertreatment(controller, req, res):
    pass


class RoomMgrQueryRoomUsersService:

    def __init__(self):
        if not hasattr(config, "ROOM_MGR_QUERY_ROOM_USERS_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_MGR_QUERY_ROOM_USERS_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_mgr_query_room_users_service_run)
        self.func_handler.pre_handler = room_mgr_query_room_users_service_pretreatment
        self.func_handler.last_handler = room_mgr_query_room_users_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.ROOM_MGR_QUERY_ROOM_USERS_SERVICE, {
        "room_id": 1
    })