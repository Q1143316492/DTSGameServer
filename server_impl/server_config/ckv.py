# coding=utf-8


def get_ckv_user_runtime(user_id):
    return "PLAYER#{}".format(user_id)


def get_ckv_room_runtime(room_id):
    return "ROOM#RUNTIME#{}".format(room_id)


# 【游戏房间】
# 记录某个游戏房间下的 玩家列表
def get_ckv_query_room_users(room_id):
    return "QUERY#ROOM#USERS#{}".format(room_id)


# 全局的房间号自增 ID
def get_ckv_server_room_id_increase():
    return "SERVER#ROOM#ID#INCREASE"


# 【玩家匹配】
# 记录真正匹配的玩家
def get_ckv_user_in_matching():
    return "USER#IN#MATCHING"


# 同步玩家帧同步类
# TODO 重构
def get_ckv_action_list(room_id):
    return "ACTION#LIST#ROOM_ID#{}".format(room_id)
