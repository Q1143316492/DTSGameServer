# coding=utf-8
from server_core.server import Server
from server_core.log import Log
from server_core.function_handler import FunctionHandler

server = None


def pre_login(req, res):
    print "pre_log" + req.msg.__str__()
    req.msg.pack_buffer(1002, "world!")


def login(req, res):
    print req.msg
    Log().info("login:test")
    res.msg = req.msg


if __name__ == '__main__':
    pass
    server = Server("cwl server", "01")

    # server.start(mode="light")
    server.start(mode="light")

    func = FunctionHandler(1001, login)
    func.pre_handler = pre_login

    server.add_handler(func)
    server.run()