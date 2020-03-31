from server_core import config
import os
import threading
import sqlite3
import hashlib


class Sqllite3(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.db_path = os.path.join(config.project_path, "database")
        self.db_name = "DTSGame.db"
        self.path = os.path.join(self.db_path, self.db_name)
        self.path = self.path.replace("\\", "/")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                cls._instance = super(Sqllite3, cls).__new__(cls)
        return cls._instance

    def connect(self):
        sqlite3.connect(self.path)


def test_md5(msg):
    print type(msg) == 'str'


if __name__ == '__main__':
    # db = Sqllite3()
    # db.connect()

    str = "asdsad"
    md5 = hashlib.md5()
    md5.update(str.encode(encoding='utf-8'))
    print md5.hexdigest()
    print len("b5b037a78522671b89a2c1b21d9b80c6")
    test_md5("sad")
    pass