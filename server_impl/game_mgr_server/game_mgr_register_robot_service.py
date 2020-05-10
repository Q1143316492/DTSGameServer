# coding=utf-8
from server_core.function_handler import FunctionHandler
from server_core.log import Log
from server_core import config
from server_impl.server_config import ckv
from server_impl.base.common import common


# 关于 robot_key 一个场景预先摆了很多AI点，所有客户端一起发起请求，但是只有一个能强度控制权，其他的负责同步
# 最终能 ret = 0 的会获得控制器，如果有控制权的客户端挂了，被心跳包干掉，其他客户端就可能获得控制器
# 客户端应该一直来抢控制器，但是频率不用特别高


def game_mgr_register_robot_service_pretreatment(controller, req, res):
    req.check_contain_int("room_id")
    req.check_contain_int("robot_key")
    req.check_contain_int("user_id")


def game_mgr_register_robot_service_run(controller, req, res):
    if not req.parse_success or not req.content:
        Log().warn("service %d req parse err %s" % (config.GAME_MGR_REGISTER_ROBOT_SERVICE, req.parse_err))
        return

    room_id = req.content["room_id"]
    robot_key = req.content["robot_key"]
    user_id = req.content["user_id"]

    born_point = 0

    ret = 0
    err_msg = ''

    room_runtime = controller.mem_cache.get(ckv.get_ckv_room_runtime(room_id))

    if room_runtime is None:
        res.content = {
            "ret": -1,
            "err_msg": "room not exist"
        }
        return

    fight_system = room_runtime.fight_system

    if robot_key in fight_system.robots_keys.keys():
        old_user_id, robot_id = fight_system.robots_keys.get(robot_key)
        if user_id != old_user_id and room_runtime.isOnline(old_user_id):
            res.content = {
                ret: -1,
                err_msg: "has been controller"
            }
            return
    else:
        robot_id = common.get_server_core(controller).get_robot_id()

    fight_system.robots_keys[robot_key] = (user_id, robot_id)
    if robot_id not in fight_system.players:
        controller.handler_dict[config.ROOM_MGR_ENTER_ROOM_SERVICE].inline_call(controller, {
            "user_id": robot_id,
            "room_type": 3,
            "room_id": room_id
        })

    res.content = {
        "ret": ret,
        "err_msg": err_msg,
        "robot_id": robot_id,
        "robot_key": robot_key,
        "born": born_point
    }


def game_mgr_register_robot_service_aftertreatment(controller, req, res):
    pass


class GameMgrRegisterRobotService:

    def __init__(self):
        if not hasattr(config, "GAME_MGR_REGISTER_ROBOT_SERVICE"):
            raise Exception("config file service id not define")
        self.handler_id = config.GAME_MGR_REGISTER_ROBOT_SERVICE
        self.func_handler = FunctionHandler(self.handler_id, game_mgr_register_robot_service_run)
        self.func_handler.pre_handler = game_mgr_register_robot_service_pretreatment
        self.func_handler.last_handler = game_mgr_register_robot_service_aftertreatment


if __name__ == '__main__':
    pass
