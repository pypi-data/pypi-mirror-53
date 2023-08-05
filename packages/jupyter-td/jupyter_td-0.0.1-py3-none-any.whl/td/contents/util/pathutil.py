#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午10:53
# File Name: pathutil.py
# Description:
# ---------------------------------------------------------------------
import os
import shutil

'''
    获取路径的工具类
'''


class PathUtil:
    @staticmethod
    def get_path(path):
        return os.path.dirname(os.path.abspath(path))

    '''
        获取绝对路径
    '''

    @staticmethod
    def absolute_path(path, *file_paths):
        for file_path in file_paths:
            path += os.sep + file_path
        return os.path.abspath(path)

    @staticmethod
    def delete_file(file_path):
        """
        删除文件夹
        :return:
        """
        try:
            shutil.rmtree(file_path)
        except Exception:
            return False
        return True


    '''
        根据路径创建文件
    '''

    @staticmethod
    def mk_dir(file_path):
        # linux或者mac的绝对路径
        if file_path.startswith('/'):
            seg = file_path.split(os.sep)[1:]
            for i in range(len(seg)):
                create_path = os.sep + os.sep.join(seg[0:i + 1])
                if not os.path.exists(create_path):
                    try:
                        os.mkdir(create_path)
                        f = open(create_path + os.sep + "__init__.py", 'w')
                        f.close()
                    except Exception:
                        return False
        # window 绝对路径 （没有测试过）或者 其余都是相对路径的情况
        else:
            seg = file_path.split(os.sep)
            for i in range(len(seg)):
                create_path = os.sep.join(seg[0:i + 1])
                if not os.path.exists(create_path):
                    try:
                        os.mkdir(create_path)
                        f = open(create_path + os.sep + "__init__.py", 'w')
                        f.close()
                    except Exception:
                        return False
        return True


    @staticmethod
    def mk_dir_with_no_initpy(file_path):
        # linux或者mac的绝对路径
        if file_path.startswith('/'):
            seg = file_path.split(os.sep)[1:]
            for i in range(len(seg)):
                create_path = os.sep + os.sep.join(seg[0:i + 1])
                if not os.path.exists(create_path):
                    try:
                        os.mkdir(create_path)
                    except Exception:
                        return False
        # window 绝对路径 （没有测试过）或者 其余都是相对路径的情况
        else:
            seg = file_path.split(os.sep)
            for i in range(len(seg)):
                create_path = os.sep.join(seg[0:i + 1])
                if not os.path.exists(create_path):
                    try:
                        os.mkdir(create_path)
                    except Exception:
                        return False
        return True

    '''
        windows的绝对路径
    '''

    @staticmethod
    def is_windows_absolute_path(filepath):
        for num in range(65, 91):
            if filepath.upper().startswith(chr(num) + ":"):
                return True
        return False