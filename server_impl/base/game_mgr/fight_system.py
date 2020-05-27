# coding=utf-8
import game_role
from game_role import Player
from server_impl.base.common import common


class FightSystem:

    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}   # int => Player

        self.robots_keys = {}  # robots_key => user_id
        # self.robots = {}
        
        self.born_point = 0

        self.goal_panel = {}

    def add_hp(self, user_id, hp):
        if user_id not in self.players:
            return
        self.players[user_id].add_hp(hp)

    def get_player(self, user_id):
        if user_id in self.players:
            return self.players[user_id]
        return None

    def query_player_born_point(self, user_id):
        if user_id not in self.players.keys():
            return None
        return self.players[user_id].born_point

    def add_player(self, player_id):
        if player_id not in self.players:
            if player_id < 0:
                born_point = self.born_point
                self.born_point += 1
            else:
                born_point = 0
            self.players[player_id] = Player(born_point)

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]

    def attacked(self, attack_id, player_id, hp):
        if self.room_id == 0:   # 0表示 游戏大厅，客户端不会发攻击命令，双保险
            return
        if self.victory():
            return
        self.check_hp(attack_id, player_id, hp)

    # attack_id 攻击 player_id 造成了 hp 伤害
    def check_hp(self, attack_id, player_id, hp):
        if player_id in self.players:
            player = self.players[player_id]
            pre_state = player.alive
            player.attacked(hp)
            # attack_id < 0 用户环境造成的伤害
            if attack_id > 0 and pre_state is True and player.alive is False:
                if attack_id in self.goal_panel:
                    self.goal_panel[attack_id] += 1
                else:
                    self.goal_panel[attack_id] = 1

    def get_gaol(self, user_id):
        if user_id in self.goal_panel:
            return self.goal_panel[user_id]
        return 0

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
        # print "#".join(msg_list)
        return "#".join(msg_list)
