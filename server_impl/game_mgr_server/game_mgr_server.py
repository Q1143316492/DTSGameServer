# coding=utf-8
from game_mgr_play_alone_service import GameMgrPlayAloneService
from game_mgr_play_with_others_service import GameMgrPlayWithOthersService
from game_mgr_query_matching_result_service import GameMgrQueryMatchingResultService
from server_impl.game_mgr_server.game_mgr_player_event_service import GameMgrPlayerEventService
from server_impl.game_mgr_server.game_mgr_fight_system_service import GameMgrFightSystemService
from game_mgr_register_robot_service import GameMgrRegisterRobotService
from game_mgr_query_born_point_service import GameMgrQueryBornPointService


class GameMgrServer:

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

        game_mgr_play_alone_service = GameMgrPlayAloneService()
        self.server.add_handler(game_mgr_play_alone_service.func_handler)

        game_mgr_play_with_others_service = GameMgrPlayWithOthersService()
        self.server.add_handler(game_mgr_play_with_others_service.func_handler)

        game_mgr_query_matching_result_service = GameMgrQueryMatchingResultService()
        self.server.add_handler(game_mgr_query_matching_result_service.func_handler)

        game_mgr_player_event_service = GameMgrPlayerEventService()
        self.server.add_handler(game_mgr_player_event_service.func_handler)

        game_mgr_fight_system_service = GameMgrFightSystemService()
        self.server.add_handler(game_mgr_fight_system_service.func_handler)

        game_mgr_register_robot_service = GameMgrRegisterRobotService()
        self.server.add_handler(game_mgr_register_robot_service.func_handler)

        game_mgr_query_born_point_service = GameMgrQueryBornPointService()
        self.server.add_handler(game_mgr_query_born_point_service.func_handler)