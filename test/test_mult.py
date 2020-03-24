# coding=utf-8
import multiprocessing.pool
import os
import random
import time


def first_progress():
    while True:
        pass
        # print os.getpid()
        # print "asd"


if __name__ == '__main__':

    p1 = multiprocessing.Process(target=first_progress)
    p2 = multiprocessing.Process(target=first_progress)

    p1.start()
    p2.start()

    print time.time()

