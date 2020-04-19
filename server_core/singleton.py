# coding=utf-8


import threading


# just a demo
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self, x, name):
        self.x = x
        print x

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:  # 加锁
                print args
                print kwargs
                cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __init__(cls, class_name, class_bases, class_dic):
        super(SingletonType, cls).__init__(class_name, class_bases, class_dic)

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


if __name__ == '__main__':
    a = Singleton(1, name="cwl")
    b = Singleton(2, name="haha")
