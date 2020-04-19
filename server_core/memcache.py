# coding=utf-8
import multiprocessing
import threading


class LockHandler:

    def __init__(self, cache, key):
        if not isinstance(cache, MemCache):
            raise TypeError("except instance MemCacheMultiProcess")
        self.cache = cache
        self.key = key
        self.is_lock = False

    def __enter__(self):
        self.is_lock = self.cache.lock_key(self.key)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_lock:
            self.cache.unlock_key(self.key)


class MemCache(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:  # 加锁
                cls._instance = super(MemCache, cls).__new__(cls)
                cls._lock = threading.Lock()
                cls._dict = dict()
                cls.lock_dict = dict()
        return cls._instance

    # 对外给 witch调用
    def lock(self, key):
        return LockHandler(self, key)

    def lock_key(self, key):
        if key not in self._dict:
            return False
        self.lock_dict[key] = threading.Lock()
        self.lock_dict[key].acquire()
        return True

    def unlock_key(self, key):
        if key not in self._dict:
            return False
        self.lock_dict[key].release()
        self.lock_dict[key] = None
        return True

    def set(self, key, val):
        self._dict[key] = val

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        return None

    def remove(self, key):
        if key in self._dict:
            del self._dict[key]

    def compare_and_set(self, key, except_val, set_val):
        ret = False
        self._lock.acquire()
        if key in self._dict and self._dict[key] == except_val:
            self._dict[key] = set_val
            ret = True
        self._lock.release()
        return ret

