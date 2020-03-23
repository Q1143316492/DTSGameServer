# coding=utf-8
from server_core.server import Server
from server_core.log import Log

server = None


def login(req, res):
    print req.msg
    Log().info("login:test")
    res.msg = req.msg


if __name__ == '__main__':
    pass
    server = Server("cwl server", "01")

    server.start()
    server.add_handler(1001, login)
    server.run()