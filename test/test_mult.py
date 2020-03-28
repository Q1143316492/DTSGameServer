# coding=utf-8
import binascii
import multiprocessing.pool
import os
import random
import struct
import time


class FunctionHandler:

    def __init__(self):
        self.pre_handler = None
        self.handler = None
        self.last_handler = None

    def call(self):
        if not self.pre_handler():
            self.pre_handler()


if __name__ == '__main__':
    print "%.2f %.2f" % (3.1415926, 66666666.66666666)
    # val = struct.pack(">i", 0x0102)
    # print binascii.hexlify(val)