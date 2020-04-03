# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
import json


def room_query_user_belonged_room_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")


def room_query_user_belonged_room_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_QUERY_USER_BELONGED_ROOM_SERVICE, req.parse_err))
        return

    Log().debug("room_query_user_belonged_room_service service: " + str(req.msg))

    # 获取参数
    user_id = str(req.content["user_id"])
    err_msg = ""

    # 处理业务

    query_ret = controller.mem_cache.get(ckv.get_ckv_user_enter_room(user_id))
    sub_server_id, room_type, room_id = -1, -1, -1
    if query_ret is not None:
        sub_server_id, room_type, room_id = query_ret.split("#")
    else:
        err_msg = "room_query_user_belonged_room_service query error"

    # 设置返回 dict
    res.content = {
        "ret": 0,
        "sub_server_id": sub_server_id,
        "room_type": room_type,
        "room_id": room_id,
        "err_msg": err_msg
    }


def room_query_user_belonged_room_service_aftertreatment(controller, req, res):
    pass


class RoomQueryUserBelongedRoomService:

    def __init__(self):
        if not hasattr(config, "ROOM_QUERY_USER_BELONGED_ROOM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_QUERY_USER_BELONGED_ROOM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_query_user_belonged_room_service_run)
        self.func_handler.pre_handler = room_query_user_belonged_room_service_pretreatment
        self.func_handler.last_handler = room_query_user_belonged_room_service_aftertreatment

