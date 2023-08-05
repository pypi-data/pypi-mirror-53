#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------
# Create Time :2019/8/13 17:50
# Author      :mqj
# File Name   :task_yaml
# Description :
#----------------------------------
#
import json
import logging
import os
import subprocess
import traceback

import requests
import yaml
from td.contents.util.config import conf

public_key_path = os.environ['HOME']+"/.ssh/id_rsa.pub"
private_key_path = os.environ['HOME'] + "/.ssh/id_rsa"
butler_url = conf.get("butler_url")


# butler_url = "http://10.59.14.213:8088"
# butler_url=conf.get("butler_url")
log =logging.getLogger("task_yaml")

def gitlab_info(path):
    os.system('cd ' + path)
    gitlab_commit_id = None
    gitlab_url = None
    gitlab_public_key = None
    gitlab_private_key = None
    gitlab_project_name = None
    gitlab_project_id = None

    (retcode, output) = subprocess.getstatusoutput('git remote -v |grep push')
    if retcode == 0:
        gitlab_url = output.split()[1]
        gitlab_project_name = gitlab_url.rsplit("/",1)[1].split(".")[0]
        gitlab_project_id = 123
    else:
        raise OSError("当前目录不是一个git仓库！")
    (retcode, output) = subprocess.getstatusoutput('git rev-parse HEAD')
    if retcode == 0:
        gitlab_commit_id = output
    else:
        raise OSError("当前目录不是一个git仓库！")
    # with open(public_key_path, "r") as fr:
    #     gitlab_public_key = fr.read()
    gitlab_public_key = " "
    with open(private_key_path, "r") as fr:
        gitlab_private_key = fr.read()

    return gitlab_url, gitlab_commit_id, gitlab_project_name, gitlab_project_id, gitlab_public_key, gitlab_private_key


def tdml_run(job_name="test",job_describe="this is a test",entry_points=[

    {
        "name":"stage1",
        "type": "python",
        "command":"python stage1.py --arg1 arg1",
        "dependence":["load_rae_data"],
        "resource":{
            "cpu":1,
            "mem":2,
            "gpu":2
        }
    }
    ,

    {
        "name":"stage2",
        "type": "python",
        "command":"python stage2.py --arg1 arg1",
        "dependence":["stage1"],
        "resource":{
            "cpu":1,
            "mem":2,
            "gpu":2
        }
    }


]):

    ipynbfile_path = os.getcwd()
    try:
        (gitlab_url, gitlab_commit_id, gitlab_project_name, gitlab_project_id, gitlab_public_key, gitlab_private_key) = gitlab_info(ipynbfile_path)
        user_name = os.getenv("user_name")
        if user_name is None:
            user_name = "test_user_name"
        else:
            user_name = user_name.split("@")[0]
        tasks = []
        task_type_dic = {'python': 0, 'horovod': 1, 'dask': 2, 'spark': 3, 'automl':4}

        for i in range(len(entry_points)):
            entry_point = entry_points[i]
            stage_name = entry_point.get("name")
            stage_type = task_type_dic.get(entry_point.get("type").lower(), 100)
            if stage_type == 100:
                raise OSError("任务类型只支持{python、horovod、dask、spark、automl}")
            stage_command = entry_point.get("command")
            if stage_type == 1:
                stage_command = "mpirun --allow-run-as-root -x NCCL_DEBUG=INFO "+stage_command
            stage_dependence = entry_point.get("dependence")
            stage_cpu = 1
            stage_mem = 2
            stage_gpu = 0
            try:
                stage_cpu = entry_point.get("resource").get("cpu")
                stage_mem = entry_point.get("resource").get("mem")
                stage_gpu = entry_point.get("resource").get("gpu")
            except Exception as e:
                log.debug("do not have cpu/mem/gpu num")
            task = {
                "taskName":stage_name,
                "taskType":stage_type,
                "taskCpu":stage_cpu,
                "taskMem":stage_mem,
                "taskGpu":stage_gpu,
                "taskCommand":stage_command,
                "taskDependence":stage_dependence
            }
            tasks.append(task)
        data = {
            "jobName": job_name,
            "jobDescribe": job_describe,
            "jobAuthor": user_name,
            "projectName": gitlab_project_name,
            "projectId": gitlab_project_id,
            "url": gitlab_url,
            "commitId": gitlab_commit_id,
            "sshPublicKey": gitlab_public_key,
            "sshPrivateKey": gitlab_private_key,
            "taskCreateRequestList": tasks
        }
        headers = {"Content-Type": "application/json"}
        print(json.dumps(data))
        r = requests.post(butler_url + "/job/create", data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            print (json.loads(r.text))
            print ("")
            print ("任务提交成功")
        else:
            print ("任务提交失败")
    except requests.exceptions.ConnectionError as e:
        print(u"请检查网络情况！")
        print(u"traceback.format_exc():\n%s" % traceback.format_exc())
    except Exception as e:
        print(u"traceback.format_exc():\n%s" % traceback.format_exc())

    return True


def butler_submit_yaml(file_path):
    y = ""
    with open(file_path) as f:
        y = yaml.load(f)

    ipynbfile_path = os.getcwd()
    try:
        job_name = y.get('name')
        job_describe = y.get('describe')
        entry_points = y.get('entry_points')

        (gitlab_url, gitlab_commit_id, gitlab_project_name, gitlab_project_id, gitlab_public_key, gitlab_private_key) = gitlab_info(ipynbfile_path)
        user_name = os.getenv("user_name")
        if user_name is None:
            user_name = "test_user_name"
        else:
            user_name = user_name.split("@")[0]

        task_type_dic = {'python': 0, 'horovod': 1, 'dask': 2, 'spark': 3, 'automl': 4}
        tasks = []
        for k,v in entry_points.items():
            entry_point = v
            stage_name = k
            stage_type = task_type_dic.get(entry_point.get("type").lower(), 100)
            if stage_type == 100:
                raise OSError("任务类型只支持{python、horovod、dask、spark、automl}")
            stage_command = entry_point.get("command")
            if stage_type == 1:
                stage_command = "mpirun --allow-run-as-root -x NCCL_DEBUG=INFO "+stage_command
            stage_dependence = entry_point.get("dependence")

            stage_cpu = 1
            stage_mem = 2
            stage_gpu = 0
            try:
                stage_cpu = entry_point.get("resource").get("cpu")
                stage_mem = entry_point.get("resource").get("mem")
                stage_gpu = entry_point.get("resource").get("gpu")
            except Exception as e:
                log.debug("do not have cpu/mem/gpu num")
            task = {
                "taskName": stage_name,
                "taskType": stage_type,
                "taskCpu": stage_cpu,
                "taskMem": stage_mem,
                "taskGpu": stage_gpu,
                "taskCommand": stage_command,
                "taskDependence": stage_dependence
            }
            tasks.append(task)

        data = {
            "jobName": job_name,
            "jobDescribe": job_describe,
            "jobAuthor": user_name,
            "projectName": gitlab_project_name,
            "projectId": gitlab_project_id,
            "url": gitlab_url,
            "commitId": gitlab_commit_id,
            "sshPublicKey": gitlab_public_key,
            "sshPrivateKey": gitlab_private_key,
            "taskCreateRequestList": tasks
        }
        headers = {"Content-Type": "application/json"}

        # print(json.dumps(data))

        r = requests.post(butler_url + "/job/create", data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            if r.json()['success'] is True:
                print (json.loads(r.text))
                print ("")
                print ("任务提交成功")
            else:
                print(u"任务提交成功，但创建失败，失败原因：%s 。" % r.json()['message'])
        else:
            print(u"任务提交失败，提交失败错误码：%s 。" % str(r.status_code))



    except requests.exceptions.ConnectionError as e:
        print(u"请检查网络情况！")
        print(e)
    except Exception as e:
        print(e)




if __name__ == '__main__':
    butler_submit_yaml("config.yml")

