#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------
# Create Time :2019/3/26 19:15
# Author      :mqj
# File Name   :resource_view
# Description :
# ----------------------------------
#
import threading
from time import sleep

import ipywidgets as widgets
import psutil
from IPython.core.display import display
from ipywidgets import Layout
from sidecar import Sidecar


def get_cpu_state(interval=1):
    return psutil.cpu_percent(interval)


def get_memory_state():
    phymem = psutil.virtual_memory()
    return int(phymem.used / 1024 / 1024), int(phymem.total / 1024 / 1024), phymem.percent


def get_gpu_state():
    print("gpu_state")


def run_proc(cpu_current, memory_current, cpu_state, memory_state):
    while True:
        cpu_current.value = get_cpu_state()
        cpu_current.max = 100
        memory_used, memory_total, memory_util = get_memory_state()
        memory_current.value = memory_used
        memory_current.max = memory_total
        cpu_state.set_title(0, u"CPU利用率:" + str(get_cpu_state()) + "%")
        memory_state.set_title(0, u"内存利用率:" + str(memory_util) + "%")
        sleep(0.5)


def resource_view():
    cpu_current = widgets.IntProgress(value=0, min=0, max=10, step=1, description=u'cpu:',
                                      bar_style='success',
                                      orientation='horizontal',
                                      layout=Layout(width='auto'))
    memory_current = widgets.IntProgress(value=0, min=0, max=10, step=1, description=u'内存:',
                                         bar_style='success',
                                         orientation='horizontal',
                                         layout=Layout(width='auto'))
    memory_box = widgets.VBox([memory_current])

    cpu_state = widgets.Accordion(children=[cpu_current])
    memory_state = widgets.Accordion(children=[memory_box])
    sidecar = Sidecar(title=u'资源情况')
    with sidecar:
        display(cpu_state)
        display(memory_state)

    new_thread = threading.Thread(target=run_proc, args=(cpu_current, memory_current, cpu_state, memory_state))
    new_thread.start()


if __name__ == "__main__":
    print(get_cpu_state())
    print(get_memory_state())
