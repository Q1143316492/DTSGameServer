# _*_coding:utf-8_*_
import logging
import threading
import time
import os
import server_core.config

log_path = os.path.join(server_core.config.project_path, 'logs')

if not os.path.exists(log_path): os.mkdir(log_path)


def format_log_str(level, msg):
    pre_str = time.strftime("|%Y-%m-%d_%H-%M-%S|", time.localtime())
    pre_str += "%s|" % level
    msg = pre_str + " " + msg.__str__()
    return msg


class Log(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.file_name = time.strftime("DTSGameServer-%Y-%m-%d.log", time.localtime())
        self.logger = logging.getLogger("core")
        self.logger.setLevel(logging.DEBUG)

    def set_level_debug(self):
        self.logger.setLevel(logging.DEBUG)

    def set_level_info(self):
        self.logger.setLevel(logging.INFO)

    def set_level_warn(self):
        self.logger.setLevel(logging.WARN)

    def set_level_error(self):
        self.logger.setLevel(logging.ERROR)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def output(self, level, msg):
        msg = format_log_str(level, msg)
        fh = logging.FileHandler(os.path.join(log_path, self.file_name), 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        if level == "debug":
            self.logger.debug(msg)
        elif level == "info":
            self.logger.info(msg)
        elif level == "warn":
            self.logger.warn(msg)
        elif level == "error":
            self.logger.error(msg)

        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()

    def debug(self, msg):
        self.output("debug", msg)

    def info(self, msg):
        self.output("info", msg)

    def warn(self, msg):
        self.output("warn", msg)

    def error(self, msg):
        self.output("error", msg)

