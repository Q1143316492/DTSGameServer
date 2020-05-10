# _*_coding:utf-8_*_
import json
import threading
import os
import errno

project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))).replace("\\", "/")
config_path = os.path.join(project_path, "config").replace("\\", "/")

# ======================================================================================================================
# server state
SERVER_STOP = 0
SERVER_ESTABLISHED = 1
SERVER_RUN = 2

# server mode

SERVER_MODE_EASY = 0
SERVER_MODE_SELECT = 1
SERVER_MODE_EPOLL = 2

# ======================================================================================================================
# net
MAX_LISTEN_QUEUE_SIZE = 65536

MAX_MESSAGE_SIZE = 1024
# NET_STATE_STOP = 0  # state: init value
# NET_STATE_CONNECTING = 1  # state: connecting
# NET_STATE_ESTABLISHED = 2  # state: connected

NET_HOST_DEFAULT_TIMEOUT = 70

NET_CONNECTION_POOL_SIZE = 100

ERR_D = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
ERR_CONN = (errno.EISCONN, 10057, 10035)  # client 10053

# ======================================================================================================================
# handler

ECHO_SERVER = 1000

USER_LOGIN_SERVICE = 1001
USER_REGISTER_SERVICE = 1002
USER_CHANGE_PASSWORD_SERVICE = 1003

ROOM_MGR_ENTER_ROOM_SERVICE = 1010
ROOM_MGR_QUERY_ROOM_USERS_SERVICE = 1011
ROOM_MGR_QUERY_USER_BELONGED_ROOM_SERVICE = 1012
ROOM_MGR_REGISTER_A_ROOM_SERVICE = 1013
ROOM_MGR_EXIST_ROOM_SERVICE = 1014

SYNCHRONIZATION_QUERY_USER_TRANSFORM_SERVICE = 1020
SYNCHRONIZATION_REPORT_TRANSFORM_SERVICE = 1021
SYNCHRONIZATION_HEART_BEAT_SERVICE = 1022
SYNCHRONIZATION_REPORT_ACTION_SERVICE = 1023
SYNCHRONIZATION_QUERY_ACTION_SERVICE = 1024

GAME_MGR_PLAY_ALONE_SERVICE = 1030
GAME_MGR_PLAY_WITH_OTHERS_SERVICE = 1031
GAME_MGR_QUERY_MATCHING_RESULT_SERVICE = 1032
GAME_MGR_PLAYER_EVENT_SERVICE = 1033
GAME_MGR_FIGHT_SYSTEM_SERVICE = 1034
GAME_MGR_REGISTER_ROBOT_SERVICE = 1035
GAME_MGR_QUERY_BORN_POINT_SERVICE = 1036

# =====================================================================================================================

GLOBAL_TOOLS = "GLOBAL_TOOLS#ASDKLJQWDNZXMC"
GLOBAL_CACHE_TOOLS = "GLOBAL_CACHE#ASDJIQWLUJDJKS"
GLOBAL_EVENT_TOOLS = "GLOBAL_EVENT#ASDQWEXCXZCLKJ"
GLOBAL_FUNC_DICT = "GLOBAL_FUNC_DICT#ASDSDASDASDASD"

# =====================================================================================================================


# 只支持加载json配置表
class ConfigLoader(object):
    _instance_lock = threading.Lock()
    is_load = False

    def __init__(self):
        self.config_contain = ""
        self.config_dict = {}
        if not ConfigLoader.is_load:
            self.load(os.path.join(config_path, "core.json").replace("\\", "/"))

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def load(self, path):
        with open(path, "r") as openfile:
            self.config_contain = openfile.read()
            self.config_dict = json.loads(self.config_contain)

    def get(self, key, default_val=None):
        if key in self.config_dict:
            return self.config_dict[key]
        return default_val

    def get_int(self, key, default_val=0):
        if key in self.config_dict:
            try:
                val = int(self.config_dict[key])
            except Exception as e:
                return default_val
            return val
        return default_val
