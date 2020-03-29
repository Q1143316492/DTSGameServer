# coding=utf-8


class ServerCreator:

    def __init__(self, filepath):
        self.filepath = filepath

    def create_server(self):
        with open(self.filepath, "r") as openfile:
            contain = openfile.read()
            print contain


if __name__ == '__main__':
    ServerCreator("../server_temple/user_server/user_server.py").create_server()