# coding=utf-8
import time
from server_core import config
from server_core.event_controller import DelayEvent
from server_impl.base.room_mgr import game_room
from server_impl.server_config import ckv


class HeartBeat:

    def __init__(self, user_id):
        self.last_tick_time = time.time()
        self.user_id = user_id

    def tick(self, controller, life_time):
        self.last_tick_time = time.time()
        controller.events.start_delay_event(DelayEvent(
            config.SYNCHRONIZATION_HEART_BEAT_SERVICE,
            {
                "user_id": self.user_id,
                "mode": 2,
                "time": self.last_tick_time,
            },
            life_time * 2
        ))

    def check(self, controller, last_tick_time):
        if abs(self.last_tick_time - last_tick_time) < 1e-3:
            game_room.out_of_last_room(controller, self.user_id)
            return False
        return True


class GameRole:

    def __init__(self):
        self.position = None
        self.rotation = None

    def set_transform(self, position=None, rotation=None):
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation

    def get_transform(self):
        return self.position, self.rotation


class UserRuntime:

    def __init__(self, user_id):
        self.user_id = int(user_id)  # 不出逻辑bug 这个 int 不会异常的
        self.room_type = None
        self.room_id = None
        self.heart_beat = HeartBeat(user_id)
        self.role = GameRole()

    def restart(self):
        self.role = GameRole()

    def set_room(self, room_type, room_id):
        self.room_type = room_type
        self.room_id = room_id

    def get_room(self):
        return self.room_type, self.room_id

    def clear(self):
        self.room_id = self.room_type = None
        self.role = None
