# coding=utf-8


def get_ckv_user_runtime(user_id):
    return "PLAYER#{}".format(user_id)


def get_ckv_room_runtime(room_id):
    return "ROOM#RUNTIME#{}".format(room_id)


# 全局的房间号自增 ID
def get_ckv_server_room_id_increase():
    return "SERVER#ROOM#ID#INCREASE"


# 【玩家匹配】
# 记录正在匹配的玩家
def get_ckv_user_in_matching():
    return "USER#IN#MATCHING"

