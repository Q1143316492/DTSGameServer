# coding=utf-8
from user_login_service import UserLoginService
from user_register_service import UserRegisterService


class UserServer:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):

        user_login_service = UserLoginService()
        self.server.add_handler(user_login_service.func_handler)

        user_register_service = UserRegisterService()
        self.server.add_handler(user_register_service.func_handler)


