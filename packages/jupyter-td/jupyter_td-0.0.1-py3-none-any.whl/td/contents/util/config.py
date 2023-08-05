#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午5:16
# File Name: config.py
# Description:
# ---------------------------------------------------------------------
# -*- coding:utf-8 -*-
import configparser
import os

'''
    读取conf配置文件信息
'''


class Config:
    def __init__(self, file_path, *items):
        config_parser = configparser.ConfigParser()
        all_items = {}
        try:
            config_parser.read(file_path)
            for item in items:
                all_items.update(config_parser.items(item))
        except Exception:
            print("没有对应的配置:", file_path, items)

        self.__dict__ = all_items

    def get(self, name):
        return self.__dict__.get(name)

    def _get(self, name, conv):
        return conv(self.get(name))

    def getint(self, name):
        return self._get(name, int)

    def getfloat(self, name):
        return self._get(name, float)

    def get_user_name(self):
        try:
            user_name = os.environ['user_name']
            index = user_name.find("@")
            if index==-1:
                return user_name
            else:
                return user_name[:index]

        except:
            raise Exception("用户不存在,联系管理员!")
    def getDCHost(self):
        return self.get('dc_host')




file_path = os.path.dirname(os.path.realpath(__file__))

import os
notebook_config = os.environ.get("TURING_NOTEBOOK_CONFIG","../conf/config-dev.conf")
conf = Config(notebook_config, "config")
tensorboard_logdir = "tensorboardlogs"

if __name__ == "__main__" :
    print(conf.get("sql_alchemy_conn"))

