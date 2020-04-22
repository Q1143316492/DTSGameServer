# coding=utf-8
from server_core.server import Server
from server_impl.synchronization_server import synchronization_server
from server_impl.room_mgr_server import room_mgr_server
from server_impl.user_server import user_server
from server_impl.game_mgr_server import game_mgr_server


if __name__ == '__main__':
    server = Server("cwl server", "01")
    server.start(mode="light")

    # 加载 service
    user_server.UserServer(server)
    room_mgr_server.RoomMgrServer(server)
    game_mgr_server.GameMgrServer(server)
    synchronization_server.SynchronizationServer(server)

    server.run()
