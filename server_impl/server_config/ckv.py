# coding=utf-8


# 【玩家】
# 记录玩家进入的房间信息
def get_ckv_user_enter_room(user):
    return "USER#ENTER#ROOM#{}".format(user)


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


# 【心跳包】
def get_ckv_heart_beat(user_id):
    return "HEART#BEAT#" + str(user_id)


# 【同步】
# 记录某个玩家 上报的 位置信息
def get_ckv_report_transform(user_id):
    return "REPORT#TRANSFORM#USER_ID#{}".format(user_id)


def get_ckv_action_list(user_id):
    return "ACTION#LIST#USER_ID#{}".format(user_id)
