# coding=utf-8
from server_core import config
from server_core.memcache import MemCache as Cache
from server_core.event_controller import EventController, DelayEvent
from server_impl.server_config import ckv
from server_impl.base.sync_mgr import frame_sync
from server_impl.base.room_mgr import game_room, room_mgr
from server_impl.base.user_mgr import user_mgr


def delay_stop_match(user_id, matching_time):
    events_controller = EventController()
    events_controller.start_delay_event(DelayEvent(
        config.GAME_MGR_PLAY_WITH_OTHERS_SERVICE,
        {
            "user_id": user_id,
            "matching_time": matching_time,
            "mode": 2
        },
        matching_time  # 单位 秒 浮点数
    ))


def start_match(user_id, matching_time):
    print "player " + str(user_id) + " begin matching."
    cache = Cache()
    key = ckv.get_ckv_user_in_matching()
    with cache.lock(key):
        matching_list = cache.get(key)
        if matching_list is None:
            matching_list = []
        if user_id not in matching_list:
            matching_list.append(user_id)
            cache.set(key, matching_list)
            delay_stop_match(user_id, matching_time)
        else:
            print "already in  matching"


def stop_match(user_id):
    print "player " + str(user_id) + " stop matching."
    cache = Cache()
    key = ckv.get_ckv_user_in_matching()
    with cache.lock(key):
        matching_list = cache.get(key)
        if matching_list is None:
            matching_list = []
        if user_id in matching_list:
            matching_list.remove(user_id)
        cache.set(key, matching_list)


def matching_some_players(controller, user_list, room_id):
    num = 0
    for user_id in user_list:
        controller.handler_dict[config.ROOM_MGR_ENTER_ROOM_SERVICE].inline_call(controller, {
            "user_id": user_id,
            "room_type": 3,
            "room_id": room_id
        })
        num += 1
        if num > 20:
            break
    sync_controller = frame_sync.FrameSync(room_id)
    controller.mem_cache.set(ckv.get_ckv_action_list(room_id), sync_controller)
    return num, 0, ""  # num, ret, err_msg


def init_room_runtime(controller, room_id):
    room_runtime_key = ckv.get_ckv_room_runtime(room_id)
    room_runtime = controller.mem_cache.get(room_runtime_key)
    if room_runtime is None:
        room_runtime = room_mgr.GameRoom(room_id)
        controller.mem_cache.set(room_runtime_key, room_runtime)
    return room_runtime


def init_user_runtime(controller, user_id):
    user_runtime_key = ckv.get_ckv_user_runtime(user_id)
    user_runtime = controller.mem_cache.get(user_runtime_key)
    if user_runtime is None:
        user_runtime = user_mgr.UserRuntime(user_id)
        controller.mem_cache.set(user_runtime_key, user_runtime)
    return user_runtime
