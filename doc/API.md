# API 接口文档

[TOC]



## 0.0 网络测试[user_network_test_service] [666]

**Request**:

| 属性名    | 类型   | 备注 |
| --------- | ------ | ---- |
| last_time | int    | ms   |
| msg       | string |      |

**Response**

| 属性名    | 类型   | 备注         |
| --------- | ------ | ------------ |
| ret       | int    | 标注请求结果 |
| err_msg   | string |              |
| last_time | int    |              |
| extend    | string |              |



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

| 属性名           | 类型   | 备注         |
| ---------------- | ------ | ------------ |
| ret              | int    | 标注请求结果 |
| register_success | bool   | 是否允许登入 |
| err_msg          | string |              |



## 1.3 修改密码[user_change_password_service] [1003]

**Request**:

| 属性名       | 类型   | 备注   |
| ------------ | ------ | ------ |
| username     | string | 用户名 |
| password     | string | 密码   |
| old_password | string | 旧密码 |

**Response**

| 属性名  | 类型   | 备注         |
| ------- | ------ | ------------ |
| ret     | int    | 标注请求结果 |
| success | bool   | 是否允许修改 |
| err_msg | string |              |

---



## 1.4 修改密码[user_level_service] [1004]

**Request**:

| 属性名  | 类型 | 备注 |
| ------- | ---- | ---- |
| user_id | int  |      |
| opt     | int  |      |
| val     | int  |      |

**Response**

| 属性名  | 类型   | 备注 |
| ------- | ------ | ---- |
| ret     | int    |      |
| err_msg | string |      |
| val     | int    |      |
| opt     |        |      |

opt == 1 上报 user_id 的 level 加 val

opt == 2 查询 user_id 的 level



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
| frame     | int  |                                                 |

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
| user_id_list | string | 玩家用户ID集合，用英文分号分隔 “;” |
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
| frame   | int  |                                                |

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



## 3.3 心跳包 [heart_beat_service] [1022]

**Request**:

| 属性名  | 类型  | 备注                                         |
| ------- | ----- | -------------------------------------------- |
| user_id | int   | 用户id                                       |
| mode    | int   | mode=1上报心跳。mode=2踢掉用户               |
| time    | float | 单位秒，浮点数，希望多久内没上报认为自己活着 |

**Response**

| 属性名  | 类型   | 备注         |
| ------- | ------ | ------------ |
| ret     | int    | 标注请求结果 |
| err_msg | string | 错误信息     |
|         |        |              |



## 3.4 行为同步 上报 [report_action_service] [1023]

同步一些射击移动动画。

**Request**:

| 属性名  | 类型   | 备注     |
| ------- | ------ | -------- |
| user_id | int    | 用户id   |
| action  | string | 表示行为 |
| frame   | int    | 上报帧   |
|         |        |          |

**Response**

| 属性名  | 类型   | 备注         |
| ------- | ------ | ------------ |
| ret     | int    | 标注请求结果 |
| err_msg | string | 错误信息     |
| frame   | int    | 下一次上报帧 |



## 3.5 行为同步 查询 [query_action_service] [1024]



同步一些射击移动动画。



**Request**:

| 属性名  | 类型 | 备注 |
| ------- | ---- | ---- |
| frame   | int  |      |
| user_id | int  |      |

**Response**

| 属性名  | 类型   | 备注                                        |
| ------- | ------ | ------------------------------------------- |
| ret     | int    | 标注请求结果                                |
| err_msg | string | 错误信息                                    |
| action  | string | 表示行为  user_id\|action#[...]#[...]#[...] |





# 4.0 游戏管理 game_mgr_server



## 4.1 开始一局人机对战[game_mgr_play_alone] [1030]

**Request**:

| 属性名  | 类型 | 备注   |
| ------- | ---- | ------ |
| user_id | int  | 用户id |
|         |      |        |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| room_id | int    |                             |



## 4.2 开启匹配模式 [game_mgr_play_with_others_service] [1031]

**Request**:

| 属性名        | 类型  | 备注                  |
| ------------- | ----- | --------------------- |
| user_id       | int   | 用户id                |
| matching_time | float | 匹配时间，单位秒      |
| mode          | int   | 1 开始匹配，2取消匹配 |

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

| 属性名  | 类型   | 备注                                                 |
| ------- | ------ | ---------------------------------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败，【-2需要重新匹配 todo】 |
| err_msg | string | 错误信息                                             |
| room_id | int    | 房间ID                                               |



## 4.4 玩家事件 [player_event_service] [1033]



**Request**:

| 属性名  | 类型   | 备注   |
| ------- | ------ | ------ |
| user_id | int    | 用户id |
| opt     | int    |        |
| event   | int    |        |
| param   | string |        |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| event   | string |                             |
| param   | string |                             |



## 4.5 战斗系统 [fight_system_service] [1034]



**Request**:

| 属性名  | 类型   | 备注   |
| ------- | ------ | ------ |
| room_id | int    | 房间id |
| opt     | string | 操作   |
| param   | string | 参数   |
|         |        |        |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| msg     | string |                             |
| opt     | string |                             |

```
[1]
opt : attacked
param : player_id, hp

[2]
opt : query_players

```

## 4.5 注册机器人 [register_robot_service] [1035]



**Request**:

| 属性名    | 类型 | 备注   |
| --------- | ---- | ------ |
| room_id   | int  | 房间id |
| robot_key | int  |        |
| user_id   | int  |        |

**Response**

| 属性名    | 类型   | 备注                               |
| --------- | ------ | ---------------------------------- |
| ret       | int    | 标注请求结果，0成功，-1失败        |
| err_msg   | string | 错误信息                           |
| robot_id  | int    | 机器人id，和用户id同作用不过是负数 |
| robot_key | int    | 机器人的key                        |
| born      | int    | 出生点编号                         |

## 4.5 查询出生点 [query_born_point] [1036]

这个还有bug

**Request**:

| 属性名  | 类型 | 备注   |
| ------- | ---- | ------ |
| room_id | int  | 房间id |
| user_id | int  |        |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| born    | int    |                             |
| user_id | int    |                             |

```
GAME_MGR_SOLVE_WEAPONS_SERVICE
```

## 4.6 维护武器 [solve_weapons_service] [1037]



**Request**:

| 属性名  | 类型 | 备注 |
| ------- | ---- | ---- |
| user_id | int  |      |
| wid     | int  |      |
|         |      |      |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| user_id | int    |                             |
| wid     | int    |                             |
|         |        |                             |



## 4.7 冻结技能 [aoe_freeze_service] [1038]



**Request**:

| 属性名  | 类型   | 备注                 |
| ------- | ------ | -------------------- |
| room_id | int    | 房间                 |
| pos     | string | vector3 split by ';' |
|         |        |                      |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| pos     | string | vector3 split by ';'        |



## 4.8 冻结技能 [new_weapon_service] [1039]



**Request**:

| 属性名  | 类型 | 备注                           |
| ------- | ---- | ------------------------------ |
| user_id | int  | user_id                        |
| w_type  | int  | 武器类型WeaponType             |
| w_pos   | int  | 武器在背包中的位置WeaponBagPos |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |
| user_id | int    |                             |
| w_type  | int    |                             |
| w_pos   | int    |                             |

## 4.8 冻结技能 [add_hp_service] [1040]



**Request**:

| 属性名  | 类型 | 备注    |
| ------- | ---- | ------- |
| user_id | int  | user_id |
| hp      | int  |         |
|         |      |         |

**Response**

| 属性名  | 类型   | 备注                        |
| ------- | ------ | --------------------------- |
| ret     | int    | 标注请求结果，0成功，-1失败 |
| err_msg | string | 错误信息                    |