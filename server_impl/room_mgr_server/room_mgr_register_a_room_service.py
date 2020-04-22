# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv


def room_mgr_register_a_room_service_pretreatment(controller, req, res):
    pass


def room_mgr_register_a_room_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.ROOM_MGR_REGISTER_A_ROOM_SERVICE, req.parse_err))
        return

    ret = 0
    room_id = 0
    err_msg = ''

    key = ckv.get_ckv_server_room_id_increase()
    with controller.mem_cache.lock(key):
        count = controller.mem_cache.get(key)

        if count is None:
            room_id = count = 1
        elif not isinstance(count, int):
            ret = -1
            room_id = -1
            err_msg = "count is not int. something happened"
        else:
            count += 1
            room_id = count
        controller.mem_cache.set(key, count)

    # 设置返回 dict
    res.content = {
        "ret": ret,
        "room_id": room_id,
        "err_msg": err_msg
    }


def room_mgr_register_a_room_service_aftertreatment(controller, req, res):
    pass


class RoomMgrRegisterARoomService:

    def __init__(self):
        if not hasattr(config, "ROOM_MGR_REGISTER_A_ROOM_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.ROOM_MGR_REGISTER_A_ROOM_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, room_mgr_register_a_room_service_run)
        self.func_handler.pre_handler = room_mgr_register_a_room_service_pretreatment
        self.func_handler.last_handler = room_mgr_register_a_room_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.ROOM_MGR_REGISTER_A_ROOM_SERVICE, {"user_id": 1})