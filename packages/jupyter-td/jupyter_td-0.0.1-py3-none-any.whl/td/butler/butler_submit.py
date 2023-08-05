#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------
# Create Time :2019/2/26 18:53
# Author      :mqj
# File Name   :submit
# Description :
# ----------------------------------
#
import json
import os
import sys
import traceback

import requests
from IPython.core.display import display, HTML
from td.contents.util.config import conf

butler_url = conf.get("butler_url")


# butler_url = "http://10.57.126.101:8088"


def submit_dlp(gpus="2",
               cpu_pernode="8",
               mem_pernode="1024",
               mpi_params="--allow-run-as-root -x NCCL_DEBUG=INFO",
               main_path="benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py",
               params=["--model resnet101", "--batch_size", "64", "--variable_update horovod"],
               workplace="/working"):
    """
    :param gpus: GPU个数
    :param cpu_pernode: CPU核数
    :param mem_pernode: 内存大小
    :param mpi_params: mpirun运行需要的参数
    :param main_path: 训练任务的主函数脚本
    :param params: 训练任务需要的参数
    :param workplace: 工作空间
    :return:
    """
    # if gpus not in ["1", "2", "4", "8", "16", "32", "64", "128", "256"]:
    #     raise ValueError("gpus 应该是1,2,4,8,16,32...")
    if not isinstance(params, list):
        raise ValueError("params应该是一维数组！")
    try:
        user_name = os.getenv("user_name")
        if user_name is None:
            user_name = "test_user_name"
        else:
            user_name = user_name.split("@")[0]
        if sys.version_info.major == 2:
            python_version = "/opt/conda2/bin/python"
        elif sys.version_info.major == 3:
            python_version = "/opt/conda3/bin/python"
        else:
            raise ValueError("未知的kernel版本!")
        data = {"gpus": gpus,
                "cpuPerNode": cpu_pernode,
                "memPerNode": mem_pernode,
                "mpiParams": mpi_params,
                "pythonVersion": python_version,
                "mainPath": main_path,
                "params": params,
                "workPlace": workplace,
                "userName": user_name}
        headers = {"Content-Type": "application/json"}
        r = requests.post(butler_url + "/task/create", data=json.dumps(data), headers=headers)
        if r.status_code == 200:
            if r.json()['resultCode'] == 0:
                if butler_url == "http://butler-production.butler.svc.cluster.local:8088":
                    butler_task_url = 'https://turing.tongdun.me/?nav=operation&option=jupyter_job&name={0}'.format(
                        user_name)
                    display(HTML(u"任务创建成功,请去Turing<a href={0}>运维中心</a>查看任务详情!".format(butler_task_url)))
                elif butler_url == "http://10.57.126.101:8088":
                    butler_task_url = 'http://10.57.125.53:8088//?nav=operation&option=jupyter_job&name={0}'.format(
                        user_name)
                    display(HTML(u"任务创建成功,请去Turing<a href={0}>运维中心</a>查看任务详情!".format(butler_task_url)))
                else:
                    display(HTML(u"任务创建成功,请去Turing运维中心查看任务详情！"))
            else:
                print(u"任务提交成功，但创建失败，失败原因：%s 。" % r.json()['value'])
        else:
            print(u"任务提交失败，提交失败错误码：%s 。" % str(r.status_code))

    except requests.exceptions.ConnectionError as e:
        print(u"请检查网络情况，或刷新butler页面，检查butler是否正常！")
        print(u"traceback.format_exc():\n%s" % traceback.format_exc())
    except Exception as e:
        print(u"traceback.format_exc():\n%s" % traceback.format_exc())


if __name__ == '__main__':
    submit_dlp("2",
               "1",
               "2048",
               "--allow-run-as-root -x NCCL_DEBUG=INFO"
               "benchmarks/scripts/tf_cnn_benchmarks/tf_cnn_benchmarks.py",
               ["--model resnet101", "--batch_size", "64", "--variable_update horovod"],
               "/working")
