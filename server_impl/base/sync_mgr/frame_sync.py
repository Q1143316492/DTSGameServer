# coding=utf-8
from server_core import config
from server_core.log import Log
from server_impl.base.room_mgr import game_room

"""
    [上一逻辑值]  ==>  允许所有客户端查询操作
    [当前逻辑帧]  ==>  接受所有客户端上报的操作     [server_frame] 执行这一帧
    即 action_table[ dict(), dict() ]  字典内容是 user_id => 操作. table_index 指向上报的帧的下标

"""


class FrameSync:

    def __init__(self, room_id):
        self.server_frame = 0
        self.room_id = room_id

        # 同步的表
        self.action_table = [dict(), dict()]
        self.report_index = 0
        self.query_table = set()

    def check_report_finish(self, controller):
        user_id_list = game_room.get_room_user_id_list(controller, self.room_id)
        if user_id_list is None:
            return False
        count = 0
        index = self.report_index
        for user_id in user_id_list:
            if user_id in self.action_table[index].keys():
                count += 1
        if count == len(user_id_list):  # 目前服务端帧已经收集到了所有的客户端信息
            return True
        return False

    def report_logic_frame(self, controller, client_frame, user_id, action):
        if client_frame == self.server_frame:
            self.action_table[self.report_index][user_id] = action
            if self.check_report_finish(controller):
                self.report_index ^= 1
                self.action_table[self.report_index] = dict()
                self.server_frame += 1
                self.query_table = set()
            return True
        return False

    def query_logic_frame(self, user_id, client_frame):
        if client_frame < self.server_frame:
            ret_list = []
            for user_id, action in self.action_table[self.report_index ^ 1].items():
                ret_list.append("|".join([str(user_id), str(action)]))
            return "#".join(ret_list)
        return None
