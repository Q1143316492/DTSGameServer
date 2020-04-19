from server_core import config


def out_of_last_room(controller, res, user_id):
    res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
        "user_id": user_id,
    })
    if res_dict["ret"] == 0:
        res.content = res_dict
        return True
    else:
        res.content = {
            "ret": res_dict["ret"],
            "err_msg": res_dict["err_msg"]
        }
        return False


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
