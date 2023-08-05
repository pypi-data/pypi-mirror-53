#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2018/11/26 下午7:27
# File Name: __init__.py
# Description:
# ---------------------------------------------------------------------
from .tlib import *
from .tools import *
# from .logging import *
from hdfs3 import HDFileSystem
import sys
import os
PY3=True
user_name = os.environ.get("user_name","").replace("@tongdun.cn", "").replace("@tongdun.net", "")
if sys.version_info.major == 2:
    PY3=False

class HDFS(HDFileSystem):
    def __init__(self):
        import subprocess
        child = subprocess.Popen("klist", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = str(child.stdout.read()) + "\n" + str(child.stderr.read())
        result = output.find("No credentials cache found")
        if result != -1:
            p = subprocess.Popen(["/usr/bin/kinit", "-kt","/etc/kerberos/mlk8s.keytab","mlk8s/gateway"], stdout=subprocess.PIPE)
            p.communicate()
        if PY3:
            super().__init__(effective_user=user_name)
        else:
            super(HDFS, self).__init__(effective_user=user_name)
    def __get_real_path(self,path):
        if path.startswith("hdfs://"):
            index = path.find("/", 7)
            if index == -1:
                path = "/"
            else:
                path = path[index:]
        return path

    def rm(self, path, recursive=True):
        path = self.__get_real_path(path)
        if not path.startswith("/user/datacompute/users/"):
            print("只允许操作个人目录下!")
        else:
            if PY3:
                super().rm(path,recursive)
            else:
                super(HDFS,self).rm(path, recursive)


    def open(self, path, mode='rb', replication=0, buff=0, block_size=0):
        path = self.__get_real_path(path)
        if not path.startswith("/user/datacompute/users/"):
            print("只允许访问操作目录下!")
        else:
            if PY3:
                return super().open(path,mode,replication,buff,block_size)
            else:
                return super(HDFS,self).open(path,mode,replication,buff,block_size)