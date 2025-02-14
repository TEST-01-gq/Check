import os
import logging

from deplog.config import LOG_PATH, LOG_FILE_NAME

log = logging.getLogger('QA.area1')
info = logging.getLogger('QA.area2')

def init_logger():
    console = logging.StreamHandler()
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, exist_ok=True)
    logFile = os.path.join(LOG_PATH, LOG_FILE_NAME)
    handler = logging.FileHandler(logFile, "a", encoding="utf-8")
    fmt = '%(asctime)s\n%(levelname)s %(filename)s %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter

    log.addHandler(handler)  # 为logger添加handler
    log.setLevel(logging.WARNING)
    log.addHandler(console)  # 屏幕只输出Warring以上日志
    info.setLevel(logging.INFO)
    info.addHandler(handler)

init_logger()