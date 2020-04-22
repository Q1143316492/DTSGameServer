# coding=utf-8
import multiprocessing

from server_core.memcache import MemCache as Cache
from server_core import config
import threading
import time
import Queue


class DelayEvent:

    # delay 单位秒 float
    def __init__(self, handler, req_dict, delay):
        self.handler = handler
        self.req_dict = req_dict
        self.run_tick = time.time() + delay

    def __lt__(self, other):
        return self.run_tick < other.run_tick


class EventController(object):

    _instance_lock = threading.Lock()

    def __init__(self, handler_dict=None):
        cache = Cache()
        self.tick = time.time()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:  # 加锁
                cls._instance = super(EventController, cls).__new__(cls)
                cls.events = Queue.PriorityQueue()
                cls.handler_dict = kwargs["handler_dict"]
        return cls._instance

    def start_delay_event(self, event):
        self.events.put(event)

    def update(self):
        self.tick = time.time()
        while not self.events.empty():
            event = self.events.get()
            if event.run_tick < self.tick:
                controller = Cache().get(config.GLOBAL_TOOLS)
                self.handler_dict[event.handler].inline_call(controller, event.req_dict)
            else:
                self.events.put(event)
                break
        pass
