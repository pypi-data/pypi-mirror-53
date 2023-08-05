#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2019/9/9 下午3:07
# File Name: tlib.py
# Description:
# ---------------------------------------------------------------------
import os
import requests
import json
import traceback
import sys
import shutil
import threading

from td.contents.util.config import conf
pid = os.getpid()
dfs_url = conf.url
tlib_url = conf.enki_url
attempt_max = int(conf.tlib_attempt_max)
threads_num = int(conf.tlib_threads_num)


class TlibThread(threading.Thread):
    def __init__(self,files,path,spark=None):
        super(TlibThread, self).__init__()
        self.path = path
        self.files = files
        self.spark = spark


    def run(self):
        for item in self.files:
            file_name = self.path + "/" + item['algoEnName'] + "." + item['algoFormat']
            algo_file_id = item['algoPkgId']
            flag = self.dfs_download(algo_file_id, file_name)
            if flag:
                if self.spark is None:
                    sys.path.append(file_name)
                else:
                    self.spark.sparkContext.addPyFile('file://' + file_name)


    def dfs_download(self,algo_file_id, file_name):
        r = requests.get("%s/%s" % (dfs_url, algo_file_id), timeout=5)
        if r.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(r.content)
            return True
        return False

def task_num(filenames):
    task_list = []
    files_num = len(filenames)
    if files_num <  threads_num:
        for i in range(1,threads_num+1):
            if i <= files_num:
                task_list.append({"index": i - 1, "len": 1})

    else:
        tasknums = int(files_num / threads_num)
        mod = files_num % threads_num
        for i in range(1,threads_num+1):
            index = (i - 1) * tasknums
            if i == threads_num:
                task_list.append({"index": index, "len": tasknums+mod})
            else:
                task_list.append({"index": index, "len":tasknums})
    return task_list

def load_tlib(env,enName=None,spark=None):
    data = {}
    headers = {"Content-Type":"application/json"}
    if enName is None:
        data = {"env":env}
    else:
        data = {"env":env,"enName":enName}

    attempt_num = 1
    status = False

    while not status and attempt_num <= attempt_max:
        try:
            r = requests.post("%s/algo/queryByEnname" % tlib_url, data=json.dumps(data), headers=headers,timeout=10)
            if r.status_code == 200:
                result = r.json()
                if result['code'] == 1000:
                    if spark is None:
                        path = "/tmp/%d" % pid
                        if os.path.exists(path):
                            shutil.rmtree(path)
                        os.makedirs(path)
                        sys.path.append(path)
                    else:
                        app_id = spark.sparkContext.applicationId
                        path = os.getcwd()+"/"+app_id
                        if os.path.exists(path):
                            shutil.rmtree(path)
                        os.makedirs(path)
                    tlibs = result['result']
                    threads = []
                    for task in task_num(tlibs):
                        start = task['index']
                        end = start + task['len']
                        t = TlibThread(tlibs[start:end],path,spark)
                        t.setDaemon(True)
                        t.start()
                        threads.append(t)

                    for t in threads:
                        t.join()
                    status = True
        except:
            msg = traceback.format_exc()
            print(msg)
        finally:
            attempt_num += 1
    if not status:
        print("算法库服务连接异常,如需算法库服务,请联系管理员")




def dfs_download(algo_file_id,file_name):
    r = requests.get("%s/%s" % (dfs_url,algo_file_id),timeout=5)
    if r.status_code == 200:
        with open(file_name,"wb") as f:
            f.write(r.content)
        return True
    return False



def query_algo_info(env,enName):
    headers = {"Content-Type":"application/json"}
    data = {"env":env,"enName":enName}
    try:
        # todo 正式上线后 网址改为读配置
        r = requests.post("%s/algo/queryByEnname" % tlib_url, data=json.dumps(data), headers=headers,timeout=10)
        if r.status_code == 200:
            result = r.json()
            if result['code'] == 1000:
                tlib = result['result']
                if len(tlib) > 0:
                    return tlib[0]
        raise Exception("not find "+ data['enName'])
    except:
        msg = traceback.format_exc()
        print(msg)
