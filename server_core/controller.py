import threading
from server_core import config


class Controller:
    _instance_lock = threading.Lock()

    def __init__(self):
        self.controller_dict = {}

    def register(self, handler, controller):
        pass