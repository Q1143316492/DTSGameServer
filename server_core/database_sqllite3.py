# coding=utf-8
from server_core import config
import os
import threading
import sqlite3
import hashlib

from server_core.log import Log


class Sqllite3:
    _instance_lock = threading.Lock()

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         with cls._instance_lock:
    #             cls._instance = super(Sqllite3, cls).__new__(cls)
    #     return cls._instance
    #
    def __init__(self):
        self.db_path = os.path.join(config.project_path, "database")
        self.db_name = "DTSGame.db"
        self.path = os.path.join(self.db_path, self.db_name)
        self.path = self.path.replace("\\", "/")

    def get_coon(self):
        try:
            conn = sqlite3.connect(self.path)
            conn.text_factory = str  # 让 原来 sqllite 返回的 unicode 设置为 str
            if os.path.exists(self.path) and os.path.isfile(self.path):
                return conn
        except Exception as e:
            Log().error("db connect create fail." + e.message)

    def get_cursor(self, conn):
        if conn is not None:
            return conn.cursor()
        else:
            return self.get_coon().cursor()

    def close_all(self, conn, cur):
        try:
            cur.close()
            conn.close()
        except Exception as e:
            Log().error("close db fail." + e.message)

    def insert(self, sql, data):
        try:
            if sql is not None and sql != '' and data is not None:
                conn = self.get_coon()
                cur = self.get_cursor(conn)
                for d in data:
                    cur.execute(sql, d)
                    conn.commit()
                rows_effect = cur.rowcount
                self.close_all(conn, cur)
                return rows_effect
            else:
                Log().warn("insert sql format fail. sql [{}] data[{}]".format(sql, data))
                return 0
        except Exception as e:
            Log().warn("insert sql format fail. sql [{}] data[{}] err:{}".format(sql, data, e.message))
            return 0

    def fetchone(self, sql, data):
        try:
            if sql is not None and sql != '' and data is not None:
                conn = self.get_coon()
                cur = self.get_cursor(conn)
                cur.execute(sql, data)
                r = cur.fetchall()
                self.close_all(conn, cur)
                return r
            else:
                Log().warn("query sql format fail. sql [{}] data[{}]".format(sql, data))
        except Exception as e:
            Log().warn("query sql format fail. sql [{}] data[{}] err:{}".format(sql, data, e.message))

    def update(self, sql, data):
        try:
            if sql is not None and sql != '' and data is not None:
                conn = self.get_coon()
                cur = self.get_cursor(conn)
                cur.execute(sql, data)
                conn.commit()
                rows_effect = cur.rowcount
                print rows_effect
                self.close_all(conn, cur)
                return rows_effect
            else:
                Log().warn("update sql format fail. sql [{}] data[{}]".format(sql, data))
                return 0
        except Exception as e:
            Log().warn("update sql format fail. sql [{}] data[{}] err:{}".format(sql, data, e.message))
            return 0


def sql_creator():
    return Sqllite3()


def test_md5():
    md5 = hashlib.md5()
    md5.update("1143316492")
    print md5.hexdigest()

    print "asdasd"[0:4]
    # print len("b5b037a78522671b89a2c1b21d9b80c6")
    # test_md5("sad")


def insert_test(db):
    sql = 'INSERT INTO [user] (username, password, salt, md5) VALUES (?, ?, ?, ?)'
    data = [
        ('netease2', '123456', 'abcd', 'b5b037a78522671b89a2c1b21d9b80c6')
    ]
    db.insert(sql, data)


def fetchone_test(db):
    fetchone_sql = 'SELECT * FROM USER WHERE user_id = ?'
    data = [7]
    db.fetchone(fetchone_sql, data)


def update_test(db):
    sql = "UPDATE [user] SET password = ? WHERE username = ?"
    data = ["123", "netease2"]
    db.update(sql, data)


if __name__ == '__main__':
    db = Sqllite3()
    # insert_test(db)
    # fetchone_test(db)
    update_test(db)

    pass