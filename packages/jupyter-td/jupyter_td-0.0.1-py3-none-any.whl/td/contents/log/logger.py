#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午10:51
# File Name: logger.py
# Description:
# ---------------------------------------------------------------------
import logging
import multiprocessing
import os
from logging.handlers import RotatingFileHandler

from td.contents.log.graylog import GraylogHandler
from td.contents.util.config import conf
from td.contents.util.pathutil import PathUtil

log_dir = conf.log_dir
log_level = logging.INFO if conf.get("log_level") == None else logging.getLevelName(conf.log_level)


class MyLogger:
    def __init__(self, logger):
        self.logger = logger
        self.logger_dict = multiprocessing.Manager().dict()

    def info(self, task_id, msg, *args, **kwargs):
        self.store_log(task_id, msg)
        self.logger.info(msg, *args, **kwargs)

    def debug(self, task_id, msg, *args, **kwargs):
        self.store_log(task_id, msg)
        self.logger.debug(msg, *args, **kwargs)

    def warn(self, task_id, msg, *args, **kwargs):
        self.store_log(task_id, msg)
        self.logger.warn(msg, *args, **kwargs)

    def error(self, task_id, msg, *args, **kwargs):
        self.store_log(task_id, msg)
        self.logger.error(msg, *args, **kwargs)

    def store_log(self, task_id, msg):
        if not isinstance(msg, str):
            msg = msg.encode('utf-8')

        self.logger_dict[task_id] = self.logger_dict.get(task_id, "") + msg + "\n"


class LoggerFactory(object):
    """
    日志工厂类
    """

    @staticmethod
    def get_logger(name, my_logger=False):
        # 获取日志文件路径
        if not os.path.isdir(log_dir + os.sep + name):
            is_ok = PathUtil.mk_dir(log_dir + os.sep + name)
            if not is_ok:
                return
        log_path = PathUtil.absolute_path(log_dir + os.sep + name, 'app.log')
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s func:%(funcName)s[line:%(lineno)d] %(levelname)s %(message)s')

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # 控制台日志
        console = logging.StreamHandler()
        console.setLevel(log_level)
        logger.addHandler(console)
        console.setFormatter(formatter)

        # 普通日志handle
        handler = RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=10)
        handler.setLevel(log_level)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # graylog handle
        graylog_handle = GraylogHandler(app='flow', file=log_path)
        logger.addHandler(graylog_handle)
        if my_logger:
            return MyLogger(logger)
        return logger


log = LoggerFactory.get_logger("flow")
my_task_log = LoggerFactory.get_logger("task", True)