# coding=utf-8
from server_core.server import Server
from server_impl.user_server import user_server
from server_impl.room_server import room_server


if __name__ == '__main__':
    server = Server("cwl server", "01")
    server.start(mode="light")

    # 加载 service
    user_server.UserServer(server)
    room_server.RoomServer(server)

    server.run()
