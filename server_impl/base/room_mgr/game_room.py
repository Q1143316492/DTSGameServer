# coding=utf-8
from server_core import config
from server_impl.base.sync_mgr import sync_mgr
from server_impl.server_config import ckv


def out_of_last_room(controller, user_id):
    res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id,
    })
    if res_dict["ret"] == 0:
        room_id = res_dict["room_id"]

        room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))
        room_runtime.remove_user(user_id)

        # TODO 房间没人的时候做一些收尾

        user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))
        user_runtime.clear()


def register_a_room(controller, user_id):
    room_id = -1
    ret = 0
    err_msg = ''
    res_dict = controller.handler_dict[config.ROOM_MGR_REGISTER_A_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id,
    })
    if res_dict["ret"] == 0:
        room_id = res_dict["room_id"]
    else:
        ret = -1
        err_msg = "try again. register room error. " + res_dict["err_msg"]
    return room_id, ret, err_msg


def get_room_user_id_list(controller, room_id):
    ret_dict = controller.handler_dict[config.ROOM_MGR_QUERY_ROOM_USERS_SERVICE].inline_call(controller, {
        "room_id": room_id
    })
    if ret_dict["ret"] != 0:
        return None
    return [int(user_id) for user_id in ret_dict["user_id_list"].split(";")]