# coding=utf-8
import os
import string
from server_core import config


server_class_content = """
class {0}:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):
    
        # example
        # [first] create service instance
        # user_login_service = UserLoginService()
        # [second] hook the service instance to this server
        # self.server.add_handler(user_login_service.func_handler)
        # todo here

"""

service_class_content = """
class {}:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):

        # example
        # [first] create service instance
        # user_login_service = UserLoginService()
        # [second] hook the service instance to this server
        # self.server.add_handler(user_login_service.func_handler)
        # todo here

"""


class ServerCreator:

    def __init__(self):
        self.folder_path = os.path.join(config.project_path, "server_temple")
        self.server_temple_path = os.path.join(self.folder_path, "server.temple").replace("\\", "/")
        self.service_temple_path = os.path.join(self.folder_path, "service.temple").replace("\\", "/")
        self.conf_dict = None
        self.server_create_folder = None
        self.server_name_list = []

    def load_config(self, conf_dict):
        self.conf_dict = conf_dict
        self.server_name_list = []
        self.server_name_list.extend(self.conf_dict["server_name"].split())
        self.server_name_list.append("server")
        self.server_create_folder = ServerCreator.create_name(self.server_name_list, 0)

    @staticmethod
    # 拼接字符串, 例如
    # user login service
    # tp == 0 结果为 user_login_service
    # tp == 1 结果为 UserLoginService
    # tp == 2 结果为 USER_LOGIN_SERVICE
    def create_name(input_list, tp=0):
        if not isinstance(input_list, list):
            raise ValueError("input_list must be list")
        if tp == 0:
            return "_".join(input_list)
        elif tp == 1:
            return "".join([word[0].upper() + word[1:].lower() for word in input_list if len(word) > 0])
        elif tp == 2:
            return "_".join([word.upper() for word in input_list if len(word) > 0])
        else:
            return ""

    def create_server(self):
        server_name = self.conf_dict["server_name"]         # 可能是多个单词
        service_list = self.conf_dict["service_list"]

        result_content = ''
        result_content += '# coding=utf-8\n'

        # 添加 import 部分代码
        for service in service_list:
            word_list = []
            word_list.extend(server_name.split(" "))
            word_list.extend(service["service_name"].split(" "))
            word_list.append("service")
            service_name_type0 = ServerCreator.create_name(word_list, 0)
            service_name_type1 = ServerCreator.create_name(word_list, 1)
            line = "from " + service_name_type0 + " import " + service_name_type1
            result_content += line + "\n"
        result_content += "\n"

        server_name_list = []
        server_name_list.extend(server_name.split())
        server_name_list.append('server')
        result_content += server_class_content.format(
            ServerCreator.create_name(server_name_list, 1))

        for service in service_list:
            word_list = []
            word_list.extend(server_name.split(" "))
            word_list.extend(service["service_name"].split(" "))
            word_list.append("service")
            service_name_type0 = ServerCreator.create_name(word_list, 0)
            service_name_type1 = ServerCreator.create_name(word_list, 1)
            result_content += '        ' + service_name_type0 + " = " + service_name_type1 + "()\n"
            result_content += '        self.server.add_handler({}.func_handler)\n\n'.format(service_name_type0)

        result_content += "\n"
        server_file_name = ServerCreator.create_name(self.server_name_list, 0) + ".py"
        with open(os.path.join(self.server_create_folder, server_file_name).replace("\\", "/"), "w") as f:
            f.write(result_content)

    def create_service(self):
        server_name = self.conf_dict["server_name"]
        service_list = self.conf_dict["service_list"]
        content = None
        with open(self.service_temple_path) as f:
            content = f.read()
            for service in service_list:
                word_list = []
                word_list.extend(server_name.split(" "))
                word_list.extend(service["service_name"].split(" "))
                word_list.append("service")
                service_name_type0 = ServerCreator.create_name(word_list, 0)
                service_name_type1 = ServerCreator.create_name(word_list, 1)
                service_name_type2 = ServerCreator.create_name(word_list, 2)
                result_content = content.format(service_name_type0, service_name_type1, service_name_type2)
                service_file_name = service_name_type0 + ".py"
                with open(os.path.join(self.server_create_folder, service_file_name).replace("\\", "/"), "w") as f:
                    f.write(result_content)

    def create_server_folder(self):
        if not os.path.exists(self.server_create_folder):
            os.makedirs(self.server_create_folder)
            print "create folder success."

    def create_init(self):
        with open(os.path.join(self.server_create_folder, "__init__.py").replace("\\", "/"), "w") as f:
            f.write("")

    def create(self):
        self.create_server_folder()
        self.create_init()
        self.create_server()
        self.create_service()


if __name__ == '__main__':

    # example
    # sc = ServerCreator()
    # sc.load_config({
    #     "server_name": "user",
    #     "service_list": [
    #         {"service_name": "login"},    # 名字有多个单词请用空格隔开
    #         {"service_name": "register"},
    #     ]
    # })
    # sc.create_server()
    # sc.create_service()

    sc = ServerCreator()

    # sc.load_config({
    #     "server_name": "user",
    #     "service_list": [
    #         # {"service_name": "login"},
    #         # {"service_name": "register"},
    #     ]
    # })
    # sc.create()

    # sc.load_config({
    #     "server_name": "room mgr",
    #     "service_list": [
    #         # {"service_name": "enter room"},
    #         # {"service_name": "query room users"},
    #         # {"service_name": "query user belonged room"},
    #         # {"service_name": "register a room"}
    #         {"service_name": "exist room"}
    #     ]
    # })
    # sc.create()

    # sc.load_config({
    #     "server_name": "synchronization",
    #     "service_list": [
    #         # {"service_name": "query user transform"},
    #         # {"service_name": "report transform"},
    #         # {"service_name": "heart beat"},
    #         # {"service_name": "report action"},
    #         # {"service_name": "query action"},
    #     ]
    # })
    # sc.create()

    sc.load_config({
        "server_name": "game mgr",
        "service_list": [
            # {"service_name": "play alone"},
            # {"service_name": "play with others"}
            # {"service_name": "query matching result"}
            # {"service_name": "player event"}
            {"service_name": "fight system"}
        ]
    })
    sc.create()