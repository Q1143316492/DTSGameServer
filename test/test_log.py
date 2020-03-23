# coding=utf-8
import time
import sys
import server_core
from server_core.log import Log
from server_core.config import ConfigLoader, project_path


if __name__ == '__main__':
    print time.strftime("%Y-%m-%d_%H:%M:%S.log", time.localtime())          # 2020-03-02_15:36:24.log
    print project_path                                                      # G:\0.workspace\DTSGame\DTSGameServer
    print server_core.log.log_path                                          # G:\0.workspace\DTSGame\DTSGameServer\logs

    log = Log()
    cp_log = Log()

    print id(log), id(cp_log)

    log.debug("sadEE")
    log.info("eee")

