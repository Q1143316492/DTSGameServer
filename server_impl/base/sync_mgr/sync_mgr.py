from server_core import config
from server_core.event_controller import DelayEvent
from server_impl.server_config import ckv


def clear_sync_msg(controller, user_id):
    controller.mem_cache.remove(ckv.get_ckv_report_transform(user_id))


def check_next_heart_beat(controller, user_id, last_time, delay_time):
    controller.events.start_delay_event(DelayEvent(
        config.SYNCHRONIZATION_HEART_BEAT_SERVICE,
        {
            "user_id": user_id,
            "mode": 2,
            "time": last_time,
        },
        delay_time * 2
    ))