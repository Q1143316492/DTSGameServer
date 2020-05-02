# coding=utf-8
from server_impl.room_mgr_server.room_mgr_enter_room_service import RoomMgrEnterRoomService
from server_impl.room_mgr_server.room_mgr_query_room_users_service import RoomMgrQueryRoomUsersService
from server_impl.room_mgr_server.room_mgr_query_user_belonged_room_service import RoomMgrQueryUserBelongedRoomService
from server_impl.room_mgr_server.room_mgr_register_a_room_service import RoomMgrRegisterARoomService
from server_impl.room_mgr_server.room_mgr_exist_room_service import RoomMgrExistRoomService


class RoomMgrServer:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):
        # example
        # [first] create service instance
        # user_login_service = UserLoginService()
        # [second] hook the service instance to this server
        # self.server.add_handler(user_login_service.func_handler)

        room_mgr_enter_room_service = RoomMgrEnterRoomService()
        self.server.add_handler(room_mgr_enter_room_service.func_handler)

        room_mgr_query_room_users_service = RoomMgrQueryRoomUsersService()
        self.server.add_handler(room_mgr_query_room_users_service.func_handler)

        room_mgr_query_user_belonged_room_service = RoomMgrQueryUserBelongedRoomService()
        self.server.add_handler(room_mgr_query_user_belonged_room_service.func_handler)

        room_mgr_register_a_room_service = RoomMgrRegisterARoomService()
        self.server.add_handler(room_mgr_register_a_room_service.func_handler)

        room_mgr_exist_room_service = RoomMgrExistRoomService()
        self.server.add_handler(room_mgr_exist_room_service.func_handler)
