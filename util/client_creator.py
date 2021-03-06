# encoding=utf-8


class_content = """
public class {0}
{{
{1}
}}
"""

struct_content = """
    [Serializable]
    public class {0}
    {{
{1}
    }}
"""

function_content = """
    public static void {0}Call({2})
    {{
        {0} request = new {0}
        {{
{3}
        }};
    
        Message message = new Message();
        message.PackBuffer(/*TODO write down service ID *//*ServiceID.XXX*/, JsonTools.SerializeToString(request));
        NetworkMgr.Instance.Send(message);
    }}
    
    public static {1} {0}Callback(Message message)
    {{
        try
        {{
            {1} response = null;
    
            response = JsonTools.UnSerializeFromString<{1}>(message.GetMessageBuffer());
    
            return response;
        }}
        catch (Exception ex)
        {{
            Debug.Log("{0}Callback parse error. " + ex.ToString());
            return null;
        }}
    }}
"""


class ClientNetworkCreator:

    def __init__(self):
        self.req_dict = {}
        self.res_dict = {}
        self.conf = {}
        self.class_name = ''
        self.req_struct_name = ''
        self.res_struct_name = ''

    def load_conf(self, conf):
        self.conf = conf

    def load_request(self, req_dict):
        self.req_dict = req_dict

    def load_response(self, res_dict):
        self.res_dict = res_dict

    def pre_solve(self):
        self.class_name = \
            "".join([word[0].upper() + word[1:].lower() for word in self.conf["class_name"].split() if len(word) > 0])
        self.req_struct_name = \
            "".join([word[0].upper() + word[1:].lower() for word in self.conf["struct_name"].split() if len(word) > 0])
        self.res_struct_name = \
            "".join([word[0].upper() + word[1:].lower() for word in self.conf["struct_name"].split() if len(word) > 0])
        self.class_name += "Router"
        self.req_struct_name += "Request"
        self.res_struct_name += "Response"

    @staticmethod
    def create_param(param_dict, pre_t):
        if not isinstance(param_dict, dict) or not isinstance(pre_t, int):
            raise Exception("create_param fail")
        content = ''
        for k, v in param_dict.items():
            content += "\t" * pre_t + "public " + v + " " + k + ";\n"
        return content

    @staticmethod
    def create_func_param(param_dict):
        content = ""
        first = True
        for k, v in param_dict.items():
            if first:
                first = False
            else:
                content += ", "
            content += v + " " + k
        return content

    @staticmethod
    def create_class_init_param(param_dict, pre_t):
        if not isinstance(param_dict, dict) or not isinstance(pre_t, int):
            raise Exception("create_class_init_param fail")
        content = ''
        for k, v in param_dict.items():
            content += "\t" * pre_t + k + " = " + k + ",\n"
        return content

    def create(self):
        self.pre_solve()
        req_content = struct_content.format(self.req_struct_name, ClientNetworkCreator.create_param(self.req_dict, 2))
        res_content = struct_content.format(self.res_struct_name, ClientNetworkCreator.create_param(self.res_dict, 2))
        content = req_content + res_content

        req_param = ClientNetworkCreator.create_func_param(self.req_dict)
        res_param = ClientNetworkCreator.create_func_param(self.res_dict)
        content += function_content.format(self.req_struct_name,
                                           self.res_struct_name,
                                           req_param,
                                           ClientNetworkCreator.create_class_init_param(self.req_dict, 3))
        print class_content.format(self.class_name, content)


def game_mgr_creator():
    cc = ClientNetworkCreator()
    # play alone service
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "play alone"
    # })
    # cc.load_request({
    #     "user_id": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string"
    # })
    # cc.create()
    # play with others
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "play with others"
    # })
    # cc.load_request({
    #     "user_id": "int",
    #     "matching_time": "float",
    #     "mode": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string"
    # })
    # cc.create()
    # query matching result
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "query matching result"
    # })
    # cc.load_request({
    #     "user_id": "int",
    #     "player_count": "int",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "room_id": "int"
    # })
    # cc.create()
    # ====================================================
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "fight system"
    # })
    # cc.load_request({
    #     "room_id": "int",
    #     "opt": "string",
    #     "param": "string"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "msg": "string"
    # })
    # cc.create()
    # =========================================================
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "register robot"
    # })
    # cc.load_request({
    #     "room_id": "int",
    #     "robot_key": "int",
    #     "user_id": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "robot_id": "int"
    # })
    # cc.create()
    # =========================================================
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "query born point"
    # })
    # cc.load_request({
    #     "room_id": "int",
    #     "user_id": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "born": "int"
    # })
    # cc.create()
    # ========================================================
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "solve weapons"
    # })
    # cc.load_request({
    #     "opt": "int",
    #     "user_id": "int",
    #     "wid": "int",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "opt": "int",
    #     "wid": "int"
    # })
    # cc.create()
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "aoe freeze"
    # })
    # cc.load_request({
    #     "room_id": "int",
    #     "pos": "string"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    # })
    # cc.create()
    # cc.load_conf({
    #     "class_name": "game mgr",
    #     "struct_name": "new weapon"
    # })
    # cc.load_request({
    #     "user_id": "int",
    #     "w_type": "int",
    #     "w_pos": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "user_id": "int",
    #     "w_type": "int",
    #     "w_pos": "int"
    # })
    # cc.create()
    cc.load_conf({
        "class_name": "game mgr",
        "struct_name": "add hp"
    })
    cc.load_request({
        "user_id": "int",
        "hp": "int"
    })
    cc.load_response({
        "ret": "int",
        "err_msg": "string",
    })
    cc.create()


def sync_server_creator():
    cc = ClientNetworkCreator()

    # cc.load_conf({
    #     "class_name": "user sync",
    #     "struct_name": "heart beat"
    # })
    # cc.load_request({
    #     "user_id": "int",
    #     "mode": "int",
    #     "time": "float",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    # })

    # ===============================================
    # cc.load_conf({
    #     "class_name": "user sync",
    #     "struct_name": "report action"
    # })
    # cc.load_request({
    #     "user_id": "int",
    #     "action": "string",
    #     "frame": "int"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "frame": "int"
    # })
    # cc.create()
    # ===============================================
    # cc.load_conf({
    #     "class_name": "user sync",
    #     "struct_name": "query action"
    # })
    # cc.load_request({
    #     "user_id": "int",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "action": "string"
    # })
    # cc.create()
    # ===============================================
    cc.load_conf({
        "class_name": "user sync",
        "struct_name": "report attack"
    })
    cc.load_request({
        "user_id": "int",
        "damage": "int",
    })
    cc.load_response({
        "ret": "int",
        "err_msg": "string"
    })
    cc.create()
    # ===============================================
    cc.load_conf({
        "class_name": "user sync",
        "struct_name": "query attack"
    })
    cc.load_request({
        "user_id": "int",
    })
    cc.load_response({
        "ret": "int",
        "err_msg": "string",
        "damage": "int"
    })
    cc.create()


def user_router_creator():
    cc = ClientNetworkCreator()
    # cc.load_conf({
    #     "class_name": "user",
    #     "struct_name": "register"
    # })
    # cc.load_request({
    #     "username": "string",
    #     "password": "string"
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "register_success": "bool"
    # })
    # cc.load_conf({
    #     "class_name": "user",
    #     "struct_name": "change password"
    # })
    # cc.load_request({
    #     "username": "string",
    #     "password": "string",
    #     "old_password": "string",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "success": "bool"
    # })
    # cc.create()

    # cc.load_conf({
    #     "class_name": "user",
    #     "struct_name": "network test"
    # })
    # cc.load_request({
    #     "last_time": "float",
    #     "msg": "string",
    # })
    # cc.load_response({
    #     "ret": "int",
    #     "err_msg": "string",
    #     "last_time": "float",
    #     "extend": "string",
    # })
    # cc.create()

    cc.load_conf({
        "class_name": "user",
        "struct_name": "user level"
    })
    cc.load_request({
        "user_id": "int",
        "opt": "int",
        "val": "int"
    })
    cc.load_response({
        "ret": "int",
        "err_msg": "string",
        "val": "int"
    })
    cc.create()


if __name__ == '__main__':
    user_router_creator()
    # game_mgr_creator()
    # sync_server_creator()
