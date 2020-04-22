from server_core import config
from server_impl.server_config import ckv


def out_of_last_room(controller, res, user_id):
    res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id,
    })
    if res_dict["ret"] == 0:
        room_id = res_dict["room_id"]
        key = ckv.get_ckv_query_room_users(room_id)
        users = controller.mem_cache.get(key)
        if users is not None:
            user_id_list = users.split(";")
            if user_id in user_id_list:
                user_id_list.remove(user_id)

            if len(user_id_list) == 0:
                controller.mem_cache.remove(key)
            else:
                controller.mem_cache.set(key, ";".join(user_id_list))

        controller.mem_cache.remove(ckv.get_ckv_user_enter_room(user_id))
        controller.mem_cache.remove(ckv.get_ckv_action_list(user_id))

        return
    else:
        res.content = {
            "ret": res_dict["ret"],
            "err_msg": "out_of_last_room fail." + res_dict["err_msg"]
        }
        return


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
