

class Player:

    def __init__(self, born_point):
        self.hp = 100
        self.alive = True
        self.belong = 0
        self.born_point = born_point

    def attacked(self, hp):
        self.hp -= max(0, hp)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
