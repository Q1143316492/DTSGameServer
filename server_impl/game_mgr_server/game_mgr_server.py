# coding=utf-8
from game_mgr_play_alone_service import GameMgrPlayAloneService
from game_mgr_play_with_others_service import GameMgrPlayWithOthersService
from game_mgr_query_matching_result_service import GameMgrQueryMatchingResultService


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