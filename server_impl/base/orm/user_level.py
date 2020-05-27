from server_impl.base.common import common
from server_core.database_sqllite3 import Sqllite3
import random


class UserLevel:

    insert_sql = 'INSERT INTO [user_level] (user_id, level) VALUES (?, ?)'
    select_sql = 'SELECT user_id, level FROM [user_level] WHERE user_id = ?'
    update_sql = 'UPDATE [user_level] SET level = ? WHERE user_id = ?'

    def __init__(self):
        self.user_id = None
        self.level = None

    def __str__(self):
        return "{}|{}".format(self.user_id, self.level)

    def insert_to_db(self):
        if not isinstance(self.user_id, int):
            return -1
        if not isinstance(self.level, int):
            return -1
        data = [
            (self.user_id, self.level)
        ]
        db = Sqllite3()
        rows_effect = db.insert(UserLevel.insert_sql, data)
        return rows_effect

    @staticmethod
    def parse_field(filed):
        user_level = UserLevel()
        user_level.user_id = filed[0]
        user_level.level = filed[1]
        return user_level

    @staticmethod
    def select_user_level_by_user_id(user_id):
        db = Sqllite3()
        ret_list = db.fetchone(UserLevel.select_sql, data=[user_id])
        if len(ret_list) != 1:
            return None
        return UserLevel.parse_field(ret_list[0])

    def update_user_level_by_user_id(self):
        if self.user_id is None or self.level is None:
            return
        db = Sqllite3()
        data = [self.level, self.user_id]
        db.update(UserLevel.update_sql, data)


if __name__ == '__main__':
    # u = UserLevel()
    # u.user_id = 1
    # u.level = 2
    # u.update_user_level_by_user_id()

    u = UserLevel.select_user_level_by_user_id(2)
    print u
