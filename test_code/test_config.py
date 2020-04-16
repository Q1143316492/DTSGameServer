# coding=utf-8
from server_core.config import ConfigLoader

if __name__ == '__main__':
    loader1 = ConfigLoader()
    loader2 = ConfigLoader()

    loader1.load("../config/core.json")
    print loader1.get("asd")
    print loader1.get("ip")

    print id(loader1), id(loader2)
