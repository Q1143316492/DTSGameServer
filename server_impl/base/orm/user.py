from server_impl.base.common import common
from server_core.database_sqllite3 import Sqllite3
import random


class User:

    insert_sql = 'INSERT INTO [user] (username, password, salt, md5) VALUES (?, ?, ?, ?)'

    select_by_user_id_sql = 'SELECT user_id, username, password, salt, md5 FROM [USER] WHERE user_id = ?'
    select_by_user_name_sql = 'SELECT user_id, username, password, salt, md5 FROM [USER] WHERE username = ?'

    update_password_by_user_id_sql = 'UPDATE [user] SET password = ?, md5 = ? WHERE user_id = ?'

    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None
        self.salt = None
        self.md5_str = None

    def __str__(self):
        return "{}|{}|{}|{}|{}".format(self.user_id, self.username, self.password, self.salt, self.md5_str)

    def insert_to_db(self):
        if not isinstance(self.username, str):
            return -1
        if not isinstance(self.password, str):
            return -1
        self.salt = common.get_md5_str(str(random.random()))[0:4]
        self.md5_str = common.get_md5_str(self.password + self.salt)
        data = [
            (self.username, self.password, self.salt, self.md5_str)
        ]
        db = Sqllite3()
        rows_effect = db.insert(User.insert_sql, data)
        return rows_effect

    @staticmethod
    def select_user_by_user_id(user_id):
        db = Sqllite3()
        ret_list = db.fetchone(User.select_by_user_id_sql, data=[user_id])
        if len(ret_list) != 1:
            return None
        return User.parse_field(ret_list[0])

    @staticmethod
    def select_user_by_user_name(username):
        db = Sqllite3()
        ret_list = db.fetchone(User.select_by_user_name_sql, data=[username])
        if len(ret_list) != 1:
            return None
        return User.parse_field(ret_list[0])

    def update_user_by_user_id(self):
        if self.user_id is None or self.password is None:
            return
        db = Sqllite3()
        self.md5_str = common.get_md5_str(self.password + self.salt)
        data = [self.password, self.md5_str, self.user_id]
        db.update(User.update_password_by_user_id_sql, data)

    @staticmethod
    def parse_field(filed):
        user_msg = User()
        user_msg.user_id = filed[0]
        user_msg.username = filed[1]
        user_msg.password = filed[2]
        user_msg.salt = filed[3]
        user_msg.md5_str = filed[4]
        return user_msg


if __name__ == '__main__':
    user = User()
    user.username = "netease3"
    user.password = "123456"
    user.insert_to_db()
    # user = User.select_user_by_user_id(7)
    print user
