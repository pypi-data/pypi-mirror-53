#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------
# Create Time :2019/4/3 13:40
# Author      :mqj
# File Name   :jupyter_resource
# Description : 
# ----------------------------------
#
import json
import os
import socket
import subprocess

from td.contents.mysql.do import JupyterResourceDo
from td.contents.mysql.repo import Repo, JupyterResourceRepo


def jupyter_resource():
    job_id = os.environ.get("jupyter_uuid")
    job_type = '0'
    user_id = os.environ.get("user_name")
    user_name = user_id.split("@")[0]
    pod_name = socket.gethostname()
    job_name = pod_name.rsplit("-", 1)[0]
    jupyter_resource_do = JupyterResourceDo()
    gpu_num = 0
    pod_restart = 0

    if pod_name.startswith("turing-gpu-notebook", 0):
        p = subprocess.Popen("nvidia-smi -L", shell=True, stdout=subprocess.PIPE)
        gpu_info_out = p.stdout.readlines()
        gpu_uuid_values = []
        for line in gpu_info_out:
            gpu_uuid_value = line.split(":")[2].replace(")", "").strip()
            gpu_uuid_values.append(gpu_uuid_value)
            gpu_num += 1
        gpu_uuid = json.dumps({"uuid": gpu_uuid_values})
        jupyter_resource_do.add_jupyter_resource(job_id, job_name, job_type, user_id, user_name, pod_name, pod_restart,
                                                 gpu_uuid, gpu_num)
    else:
        gpu_uuid = None
        jupyter_resource_do.add_jupyter_resource(job_id, job_name, job_type, user_id, user_name, pod_name, pod_restart,
                                                 gpu_uuid, gpu_num)

    repo = Repo()
    jupyter_resource_repo = JupyterResourceRepo()

    jupyter_resource_record = jupyter_resource_repo.query_by_jobid_finishtime(job_id, pod_restart)
    if jupyter_resource_record:
        jupyter_resource_repo.update(job_id, pod_restart)
        # repo.add(jupyter_resource_do) # pod重启不再新增加记录 只是更新一些时间，该时间会被正常关闭而再次更新时间
    else:
        repo.add(jupyter_resource_do)


if __name__ == '__main__':
    jupyter_resource()
