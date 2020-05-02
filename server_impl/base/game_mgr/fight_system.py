# coding=utf-8


class Player:

    def __init__(self):
        self.hp = 100
        self.alive = True

    def attacked(self, hp):
        self.hp -= max(0, hp)
        if self.hp <= 0:
            self.hp = 0
            self.alive = False


class FightSystem:

    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}   # int => Player

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = Player()

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def attacked(self, player_id, hp):
        # if self.room_id == 0:   # 0表示 游戏大厅，客户端不会发攻击命令，双保险
        #     return
        if self.victory():
            return
        if player_id in self.players:
            player = self.players[player_id]
            player.attacked(hp)
            # if not player.alive:
            #     self.remove_player(player_id)

    def victory(self):
        return len(self.players) == 1

    def query_hp(self, player_id):
        if player_id not in self.players:   # 该玩家已死
            return -1
        return self.players[player_id].hp

    def query_players_hp(self):
        msg_list = []
        for player_id, player in self.players.items():
            msg_list.append("{}|{}".format(player_id, player.hp))
        return "#".join(msg_list)
