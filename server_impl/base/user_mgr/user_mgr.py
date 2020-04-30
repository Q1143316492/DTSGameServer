# coding=utf-8


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
