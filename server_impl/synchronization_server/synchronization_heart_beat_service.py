# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
from server_impl.base.sync_mgr import sync_mgr
import time


def synchronization_heart_beat_service_pretreatment(controller, req, res):
    req.check_contain_int("user_id")
    req.check_contain_int("mode")
    req.check_contain_float("time")


def synchronization_heart_beat_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.SYNCHRONIZATION_HEART_BEAT_SERVICE, req.parse_err))
        return

    user_id = req.content["user_id"]
    mode = req.content["mode"]
    life_time = req.content["time"]     # 单位秒，浮点数

    ret = 0
    err_msg = ''

    user_runtime = ckv.get_ckv_user_runtime(user_id)
    now_time = time.time()

    if mode == 1:
        res_dict = controller.handler_dict[config.ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE].inline_call(controller, {
            "user_id": user_id,
        })
        if res_dict["ret"] == -1:
            # 某种原因客户端又连上了，但是服务端认为你已经掉线了，而且该清空的都清空了
            res.content = {
                "ret": -1,
                "err_msg": "try to reconnect"
            }
            return
        user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))
        user_runtime.heart_beat.tick(controller, life_time)
    elif mode == 2:
        user_runtime = controller.mem_cache.get(ckv.get_ckv_user_runtime(user_id))
        user_runtime.heart_beat.check(controller, life_time)

    res.content = {
        "ret": 0,
        "err_msg": ''
    }


def synchronization_heart_beat_service_aftertreatment(controller, req, res):
    pass


class SynchronizationHeartBeatService:

    def __init__(self):
        if not hasattr(config, "SYNCHRONIZATION_HEART_BEAT_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.SYNCHRONIZATION_HEART_BEAT_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, synchronization_heart_beat_service_run)
        self.func_handler.pre_handler = synchronization_heart_beat_service_pretreatment
        self.func_handler.last_handler = synchronization_heart_beat_service_aftertreatment


if __name__ == '__main__':
    from server_impl.test_client import TestClient

    TestClient.send(config.SYNCHRONIZATION_HEART_BEAT_SERVICE, {
        "user_id": 1,
        "mode": 1,
        "time": 2,
    })
