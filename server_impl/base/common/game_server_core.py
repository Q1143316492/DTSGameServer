

class GameServerCore:

    def __init__(self):
        self.robot_id = 1000

    def get_robot_id(self):
        self.robot_id += 1
        return -self.robot_id
