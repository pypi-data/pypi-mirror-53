#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/15 下午11:04
# File Name: tdlab.py
# Description:
# ---------------------------------------------------------------------
from jupyterlab.labapp import LabApp
from notebook._tz import utcnow
from zmq.eventloop import ioloop
from jupyter_core.application import NoStart
import os
import requests
ioloop.install()

from traitlets.traitlets import (
    Bool, Unicode, List, Enum, Dict, Instance, TraitError, observe, observe_compat, default,
)
import sys
import logging
import shutil

turing_url = os.environ.get("turing_url","https://turing.tongdun.cn")
user_name = os.environ.get("user_name")
jupyter_uuid = os.environ.get("jupyter_uuid")

def make_hemo_info():
    try:
        import socket
        import textwrap
        info_content = "HOSTNAME=%s\nDC=HZ\nAPPNAME=turing-jupyter\nENV=production\nCLUSTER=turing-jupyter"
        info_path = "/home/admin/output/info"
        hostname = socket.gethostname()
        info_content = info_content % hostname

        with open(info_path,"w") as f:
            f.write(info_content)
    except:
        pass


class LevelFormatter(logging.Formatter):
    """Formatter with additional `highlevel` record

    This field is empty if log level is less than highlevel_limit,
    otherwise it is formatted with self.highlevel_format.

    Useful for adding 'WARNING' to warning messages,
    without adding 'INFO' to info, etc.
    """
    highlevel_limit = logging.WARN
    highlevel_format = " %(levelname)s |"

    def format(self, record):
        if record.levelno >= self.highlevel_limit:
            record.highlevel = self.highlevel_format % record.__dict__
        else:
            record.highlevel = ""
        return super(LevelFormatter, self).format(record)

class TDLabApp(LabApp):

    @default('log')
    def _log_default(self):
        """Start logging for this application.

        The default is to log to stderr using a StreamHandler, if no default
        handler already exists.  The log level starts at logging.WARN, but this
        can be adjusted by setting the ``log_level`` attribute.
        """
        log = logging.getLogger(self.__class__.__name__)
        log.setLevel(self.log_level)
        log.propagate = False
        _log = log  # copied from Logger.hasHandlers() (new in Python 3.2)
        while _log:
            if _log.handlers:
                return log
            if not _log.propagate:
                break
            else:
                _log = _log.parent
        if sys.executable and sys.executable.endswith('pythonw.exe'):
            # this should really go to a file, but file-logging is only
            # hooked up in parallel applications
            _log_handler = logging.StreamHandler(open(os.devnull, 'w'))
        else:
            from logging.handlers import RotatingFileHandler
            from td.contents.util.config import conf
            if not os.path.exists(conf.log_dir):
                os.makedirs(conf.log_dir)
            file_handler = RotatingFileHandler(conf.log_dir+"xxxx.log", maxBytes= 100 *1024 * 1024, backupCount=2)
            _log_handler = file_handler
            _console_log_handler = logging.StreamHandler()
            log.addHandler(_console_log_handler)
        _log_formatter = self._log_formatter_cls(fmt=self.log_format, datefmt=self.log_datefmt)
        _log_handler.setFormatter(_log_formatter)
        log.addHandler(_log_handler)
        return log


    ##关闭server
    def shutdown(self):
        try:
            r = requests.post(turing_url + "/jupyterlab/delete",
                              data={"jupyter_uuid": jupyter_uuid, "user_name": user_name})
            if r.status_code == 200 and r.json()['success']:
                self.log.info("关闭成功!")
            else:
                self.log.error("server 关闭失败!")
        except Exception as e:
            self.log.error("%s,%s,%s,server 关闭失败!" % (turing_url, jupyter_uuid, user_name))
        finally:
            if os.path.exists("/tmp/td_jupyter_exception/"):
                shutil.rmtree("/tmp/td_jupyter_exception/")

    def shutdown_no_activity(self):
        """Shutdown server on timeout when there are no kernels or terminals."""
        km = self.kernel_manager
        if len(km) != 0:
            return   # Kernels still running

        try:
            term_mgr = self.web_app.settings['terminal_manager']
        except KeyError:
            pass  # Terminals not enabled
        else:
            if term_mgr.terminals:
                return   # Terminals still running

        seconds_since_active = \
            (utcnow() - self.web_app.last_activity()).total_seconds()
        self.log.debug("No activity for %d seconds.",
                       seconds_since_active)
        if seconds_since_active > self.shutdown_no_activity_timeout:
            self.log.info("No kernels or terminals for %d seconds; shutting down.",
                          seconds_since_active)
            print("------stop----")
            self.shutdown()
            # self.stop()

    def init_shutdown_no_activity(self):
        if self.shutdown_no_activity_timeout > 0:
            self.log.info("Will shut down after %d seconds with no kernels or terminals.",
                          self.shutdown_no_activity_timeout)
            pc = ioloop.PeriodicCallback(self.shutdown_no_activity, 60000)
            pc.start()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch an instance of a Jupyter Application"""
        try:
            make_hemo_info()
            return super(TDLabApp, cls).launch_instance(argv=argv, **kwargs)
        except NoStart:
            return

main = launch_new_instance = TDLabApp.launch_instance

if __name__ == '__main__':
    main()
