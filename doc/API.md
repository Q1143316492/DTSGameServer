# API 接口文档

[TOC]

# 1.0 用户管理 user_server

## 1.1 用户登入[user_login_service] [1001]

**Request**:

| 属性名   | 类型   | 备注                                           |
| -------- | ------ | ---------------------------------------------- |
| username | string | 用户名                                         |
| password | string | 密码                                           |
| time     | int    | Unity Time.time() 向下取整，毫秒级别，发包时间 |

**Response**

| 属性名        | 类型 | 备注                                           |
| ------------- | ---- | ---------------------------------------------- |
| ret           | int  | 标注请求结果                                   |
| login_success | bool | 是否允许登入                                   |
| user_id       | int  | 用户id                                         |
| time          | int  | Unity Time.time() 向下取整，毫秒级别，发包时间 |



## 1.2 用户注册[user_register_service] [1002]

**Request**:

| 属性名   | 类型   | 备注   |
| -------- | ------ | ------ |
| username | string | 用户名 |
| password | string | 密码   |

**Response**

| 属性名           | 类型 | 备注         |
| ---------------- | ---- | ------------ |
| ret              | int  | 标注请求结果 |
| register_success | bool | 是否允许登入 |



---



# 2.0 游戏房间管理 room_mgr_server

每一局游戏，都是多个玩家在同一个场景的行为。把场景定义为房间

这块接口控制玩家加入场景的行为。

## 2.1 玩家加入一个游戏场景[enter_room_service] [1010]

**note:**

游戏开始，玩家加入一个初始化的场景。在这里选择下一步游戏行为。目前先让全服玩家在同一场景

**Request**:

| 属性名    | 类型 | 备注                                            |
| --------- | ---- | ----------------------------------------------- |
| user_id   | int  | 用户id                                          |
| room_type | int  | 游戏房间类型【1 初始场景】                      |
| room_id   | int  | 【可选】room_type==3, 表示玩家加入room_id的游戏 |

ps:

初始场景：玩家登入后即进入初始场景。等待匹配正式游戏。

如果初次登入, room_type 为 1. 类似游戏大厅的概念

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果                |
| room_id | int    | 房间编号，【0】表示游戏大厅 |
| err_msg | string | 错误信息                    |



## 2.2 询问玩家所在房间有哪些其他玩家[query_room_users_service] [1011]

**note:**

游戏开始，玩家一定属于某一个游戏场景。查询该玩家所在场景有哪些玩家。

**Request**:

| 属性名  | 类型 | 备注 |
| ------- | ---- | ---- |
| room_id | int  | id   |

**Response**

| 属性名       | 类型   | 备注                               |
| ------------ | ------ | ---------------------------------- |
| ret          | int    | 标注请求结果                       |
| user_id_list | string | 玩家用户名集合，用英文分号分隔 “;” |
| err_msg      | string | 错误信息                           |



## 2.3 询问玩家所在房间[room_query_user_belonged_room_service] [1012]

**note:**

游戏开始，玩家一定属于某一个游戏场景。查询该玩家所在场景有哪些玩家。

**Request**:

| 属性名  | 类型 | 备注 |
| ------- | ---- | ---- |
| user_id | int  | id   |

**Response**

| 属性名    | 类型   | 备注         |
| --------- | ------ | ------------ |
| ret       | int    | 标注请求结果 |
|           |        |              |
| room_type | int    | 场景地图类型 |
| room_id   | int    | 房间id       |
| err_msg   | string | 错误原因     |



## 2.4 注册一个新房间[room_mgr_register_a_room_service] [1013]



**Request**:

| 属性名  | 类型 | 备注   |
| ------- | ---- | ------ |
| user_id | int  | 用户ID |

**Response**

| 属性名  | 类型   | 备注         |
| ------- | ------ | ------------ |
| ret     | int    | 标注请求结果 |
| room_id | int    | 房间id       |
| err_msg | string | 错误原因     |
|         |        |              |



## 2.5 玩家退出房间 [room_mgr_exist_room_service] [1014]



**Request**:

| 属性名  | 类型 | 备注   |
| ------- | ---- | ------ |
| user_id | int  | 用户ID |

**Response**

| 属性名  | 类型   | 备注         |
| ------- | ------ | ------------ |
| ret     | int    | 标注请求结果 |
| err_msg | string | 错误原因     |



# 3.0 游戏玩家同步管理 synchronization_server

## 3.1 询问有关玩家的信息[query_user_transform_service] [1020]

**note:**

查询某个玩家多位置信息

**Request**:

| 属性名  | 类型 | 备注                                           |
| ------- | ---- | ---------------------------------------------- |
| user_id | int  | 用户id                                         |
| time    | int  | Unity Time.time() 向下取整，毫秒级别，发包时间 |

**Response**

| 属性名   | 类型   | 备注                                           |
| -------- | ------ | ---------------------------------------------- |
| ret      | int    | 标注请求结果                                   |
| err_msg  | string | 错误信息                                       |
| position | string | 三个浮点值用分号拼接的字符串                   |
| rotation | string | 三个浮点值用分号拼接的字符串                   |
| time     | int    | Unity Time.time() 向下取整，毫秒级别，发包时间 |



## 3.2 向服务器报告自己的信息[report_transform_service] [1021]

**Request**:

| 属性名   | 类型   | 备注                                           |
| -------- | ------ | ---------------------------------------------- |
| user_id  | int    | 用户id                                         |
| position | string | 三个浮点值用分号拼接的字符串                   |
| rotation | string | 三个浮点值用分号拼接的字符串                   |
| time     | int    | Unity Time.time() 向下取整，毫秒级别，发包时间 |

**Response**

| 属性名  | 类型   | 备注                                           |
| ------- | ------ | ---------------------------------------------- |
| ret     | int    | 标注请求结果                                   |
| err_msg | string | 错误信息                                       |
| time    | int    | Unity Time.time() 向下取整，毫秒级别，发包时间 |



# 4.0 游戏管理 game_mgr_server



## 4.1 开始一局人机对战[game_mgr_play_alone] [1030]

**Request**:

| 属性名  | 类型 | 备注   |
| ------- | ---- | ------ |
| user_id | int  | 用户id |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |



## 4.2 开启匹配模式 [game_mgr_play_with_others_service] [1031]

**Request**:

| 属性名        | 类型  | 备注                  |
| ------------- | ----- | --------------------- |
| user_id       | int   | 用户id                |
| matching_time | float | 匹配时间，单位秒      |
| mode          | int   | 1 开始匹配，0取消匹配 |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |



## 4.3 请求匹配结果 [game_mgr_query_matching_result_service] [1032]



**Request**:

| 属性名       | 类型 | 备注                     |
| ------------ | ---- | ------------------------ |
| user_id      | int  | 用户id                   |
| player_count | int  | 需要多少玩家视为匹配成功 |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| room_id | int    | 房间ID                      |