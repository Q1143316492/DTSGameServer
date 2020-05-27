

class WeaponBag:

    def __init__(self):
        self.now_weapon_type = -1


class Player:

    def __init__(self, born_point):
        self.hp = 100
        self.alive = True
        self.belong = 0
        self.born_point = born_point
        self.weapons_bag = WeaponBag()

    def attacked(self, hp):
        self.hp -= max(0, hp)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def add_hp(self, hp):
        self.hp += hp
        if self.hp < 0:
            self.hp = 0
            self.alive = False
        if self.hp > 100:
            self.hp = 100