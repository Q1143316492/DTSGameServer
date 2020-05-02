# coding=utf-8
from synchronization_query_user_transform_service import SynchronizationQueryUserTransformService
from synchronization_report_transform_service import SynchronizationReportTransformService
from server_impl.synchronization_server.synchronization_heart_beat_service import SynchronizationHeartBeatService
from server_impl.synchronization_server.synchronization_report_action_service import SynchronizationReportActionService
from server_impl.synchronization_server.synchronization_query_action_service import SynchronizationQueryActionService


class SynchronizationServer:

    def __init__(self, server):
        self.server = server
        self.load_service()

    def load_service(self):
    
        # example
        # [first] create service instance
        # user_login_service = UserLoginService()
        # [second] hook the service instance to this server
        # self.server.add_handler(user_login_service.func_handler)

        synchronization_query_user_transform_service = SynchronizationQueryUserTransformService()
        self.server.add_handler(synchronization_query_user_transform_service.func_handler)

        synchronization_report_transform_service = SynchronizationReportTransformService()
        self.server.add_handler(synchronization_report_transform_service.func_handler)

        synchronization_heart_beat_service = SynchronizationHeartBeatService()
        self.server.add_handler(synchronization_heart_beat_service.func_handler)

        synchronization_report_action_service = SynchronizationReportActionService()
        self.server.add_handler(synchronization_report_action_service.func_handler)

        synchronization_query_action_service = SynchronizationQueryActionService()
        self.server.add_handler(synchronization_query_action_service.func_handler)
