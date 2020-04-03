# coding=utf-8


def get_ckv_user_enter_room(user):
    return "USER#ENTER#ROOM#{}".format(user)


def get_ckv_query_room_users(room_id):
    return "QUERY#ROOM#USERS#{}".format(room_id)