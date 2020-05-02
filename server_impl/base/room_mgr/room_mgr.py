# coding=utf-8
from server_core.log import Log
from server_impl.base.sync_mgr import frame_sync
from server_impl.base.game_mgr import fight_system


class GameRoom:

    def __init__(self, room_id):
        self.room_id = room_id
        self._sync_controller = None
        self._user_id_list = []  # 存的是 user_id 的 字符形式
        self.fight_system = fight_system.FightSystem(room_id)

    def get_sync(self):
        if self._sync_controller is None:
            self._sync_controller = frame_sync.FrameSync(self.room_id)
        return self._sync_controller

    def add_user(self, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            Log().warn("game_room id: {}, user_id {}, user_id must be int".format(self.room_id, user_id))
            return False
        if user_id not in self._user_id_list:
            self._user_id_list.append(str(user_id))
            self.fight_system.add_player(int(user_id))
            return True
        return False

    def remove_user(self, user_id):
        if user_id in self._user_id_list:
            self._user_id_list.remove(str(user_id))
            self.fight_system.remove_player(int(user_id))

    def get_user_id_list_str(self):
        return ";".join(self._user_id_list)


if __name__ == '__main__':
    pass
