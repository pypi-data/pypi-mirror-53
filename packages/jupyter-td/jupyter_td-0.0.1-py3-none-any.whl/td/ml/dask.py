#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2019/8/15 下午5:19
# File Name: dask.py
# Description:
# ---------------------------------------------------------------------
from dask_kubernetes import KubeCluster

def make_dask():
    cluster = KubeCluster.from_yaml('worker-spec.yml')
    return cluster


def build_yaml():
    new_path = '/tmp/worker-spec.yml'
    f = open("worker-spec.yml",'r',encoding='utf-8')
    f_new = open('/tmp/worker-spec.yml', 'w', encoding='utf-8')
    for line in f:

    pass