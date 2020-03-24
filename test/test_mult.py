# coding=utf-8
import multiprocessing.pool
import os
import random
import time


class FunctionHandler:

    def __init__(self):
        self.pre_handler = None
        self.handler = None
        self.last_handler = None

    def call(self):
        if not self.pre_handler():
            self.pre_handler()


def handler():
    print "handler"

if __name__ == '__main__':
    pass