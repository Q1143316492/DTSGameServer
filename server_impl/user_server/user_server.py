# coding=utf-8
from user_login_service import UserLoginService
from user_register_service import UserRegisterService
from server_impl.user_server.user_change_password_service import UserChangePasswordService
from server_impl.user_server.user_network_test_service import UserNetworkTestService
from server_impl.user_server.user_user_level_service import UserUserLevelService


class UserServer:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):

        user_login_service = UserLoginService()
        self.server.add_handler(user_login_service.func_handler)

        user_register_service = UserRegisterService()
        self.server.add_handler(user_register_service.func_handler)

        user_change_password_service = UserChangePasswordService()
        self.server.add_handler(user_change_password_service.func_handler)

        user_network_test_service = UserNetworkTestService()
        self.server.add_handler(user_network_test_service.func_handler)

        user_user_level_service = UserUserLevelService()
        self.server.add_handler(user_user_level_service.func_handler)