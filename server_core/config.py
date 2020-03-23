# _*_coding:utf-8_*_
import json
import threading
import os
import errno

project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
config_path = os.path.join(project_path, "config")

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


# =====================================================================================================================


# 只支持加载json配置表
class ConfigLoader(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.config_contain = ""
        self.config_dict = {}

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
