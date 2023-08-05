#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------
# Create Time :
# Author      :
# File Name   :
# Description :
# ----------------------------------
#
from __future__ import print_function

import json
import os
import random
import shutil
import string
import sys
import traceback
import zipfile

import requests
from td.contents.mysql.do import ProjectModelDo, LocalProjectDo, ModelBuildHistoryDo
from td.contents.mysql.repo import Repo, LocalProjectRepo, ModelBuildHistoryRepo
from td.contents.mysql.repo import project_model_repo
from td.contents.util.config import conf

from . import stderr
from . import stdout

model_build_need_file_path = ""
if sys.version_info.major == 2:
    model_build_need_file_path = u"/opt/modelfile_python2"
else:
    model_build_need_file_path = u"/opt/modelfile_python3"

execute_model_path = os.path.join(model_build_need_file_path, u'execute_model.py')
prepare_test_path = os.path.join(model_build_need_file_path, u'prepare_test.py')
init_path = os.path.join(model_build_need_file_path, u'__init__.py')

build_version = 0
created_by = os.getenv("user_name").replace("@tongdun.cn", "").replace("@tongdun.net", "")

execute_model_path_new = None
prepare_test_path_new = None
init_path_new = None
handle_data_path_new = None
params_spec_path_new = None
model_files_path_new = []


def query_local_project_info(name):
    """
    根据项目名查询项目ID
    :param name: 项目名（唯一值）
    :return: 项目信息
    """
    local_project_do = LocalProjectDo()
    local_project_do.query_local_project(name)
    local_project_repo = LocalProjectRepo()
    local_project_do_result = local_project_repo.query(local_project_do)
    return local_project_do_result


def query_model_build_history_info(name, created_by, status):
    """
    查询构建历史信息
    :param name: 模型名
    :param created_by:模型打包用户
    :return: 所有模型信息
    """
    model_build_history_do = ModelBuildHistoryDo()
    model_build_history_do.query_model_build_history(name, created_by, status)
    model_build_history_repo = ModelBuildHistoryRepo()
    query_model_build_history_result = model_build_history_repo.query(model_build_history_do)
    return query_model_build_history_result


def test_prepare(name, handle_data_path, params_spec_path, model_files, test_data):
    """
    模型打包预跑测试函数
    :param name: 模型名
    :param handle_data_path: handle_data.py文件的路径
    :param params_spec_path: params_spec.xml/csv 文件的路径
    :param model_files: 模型相关的文件（包括模型文件和自定义的函数文件）
    :param test_data: 测试数据
    :return:
    """

    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    cwd = os.path.join('/tmp', name + '-' + salt + '/')
    os.makedirs(cwd)

    if os.path.exists(os.path.join(cwd, '__init__.py')):
        os.remove(os.path.join(cwd, '__init__.py'))
    shutil.copy(init_path, cwd)
    global init_path_new
    init_path_new = os.path.join(cwd, '__init__.py')

    if os.path.exists(os.path.join(cwd, 'prepare_test.py')):
        os.remove(os.path.join(cwd, 'prepare_test.py'))
    shutil.copy(prepare_test_path, cwd)
    global prepare_test_path_new
    prepare_test_path_new = os.path.join(cwd, 'prepare_test.py')

    if os.path.exists(os.path.join(cwd, 'execute_model.py')):
        os.remove(os.path.join(cwd, 'execute_model.py'))
    shutil.copy(execute_model_path, cwd)
    global execute_model_path_new
    execute_model_path_new = os.path.join(cwd, 'execute_model.py')

    if os.path.exists(os.path.join(cwd, 'handle_data.py')):
        os.remove(os.path.join(cwd, 'handle_data.py'))
    shutil.copy(handle_data_path, cwd)
    global handle_data_path_new
    handle_data_path_new = os.path.join(cwd, 'handle_data.py')

    if os.path.exists(os.path.join(cwd, u'params_spec.xml')):
        os.remove(os.path.join(cwd, u'params_spec.xml'))
    shutil.copy(params_spec_path, cwd)
    global params_spec_path_new
    params_spec_path_new = os.path.join(cwd, u'params_spec.xml')

    global model_files_path_new
    model_files_path_new = []
    for model_file in model_files:
        model_file_path, model_file_name = os.path.split(model_file)
        if os.path.exists(os.path.join(cwd, model_file_name)):
            os.remove(os.path.join(cwd, model_file_name))
        shutil.copy(model_file, cwd)
        model_files_path_new.append(os.path.join(cwd, model_file_name))

    # sys.path.append(cwd)
    sys.path.insert(0, cwd)
    from prepare_test import test_fun
    test_fun(test_data)


def make_filezip(name):
    """
    打包成zip包
    :param name: 模型名
    :return:
    """

    filezip = zipfile.ZipFile(u'/tmp/' + name + r'.zip', "w", zipfile.ZIP_DEFLATED)

    filezip.write(init_path_new, u'__init__.py')
    filezip.write(execute_model_path_new, u'execute_model.py')
    filezip.write(prepare_test_path_new, u'prepare_test.py')

    filezip.write(params_spec_path_new, u'params_spec.xml')
    filezip.write(handle_data_path_new, u'handle_data.py')
    for model_file in model_files_path_new:
        model_file_path, model_file_name = os.path.split(model_file)
        filezip.write(model_file, model_file_name)
    filezip.close()


def upload_file(name):
    """
    上传zip包到dfs文件系统
    :param name: 模型名，用于指定zip包的路径
    :return: dfs返回的唯一ID
    """
    try:
        #py3
        from urllib.parse import quote
    except Exception as e:
        #py2
        from urllib import quote
    url = conf.get("url")
    namespace = conf.get("namespace")
    ttl = conf.get("ttl")
    upload_file_path = os.path.join(r'/tmp', name + r'.zip')
    filesize = os.path.getsize(upload_file_path)
    files = {name: (name, open(upload_file_path, 'rb'))}
    data = {'namespace': namespace, 'length': filesize, 'name': quote(name) + '.zip', 'ttl': ttl}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        file_id = response.json()["data"]
        return file_id
    else:
        print("status_code:{}:".format(response.status_code))
        sys.exit(1)

def upload_file_to_hdfs(name,create_by):
    """
    上传zip包到HDFS文件系统
    :param name: 模型名，用于指定zip包的路径
    :return: dfs返回的唯一ID
    """
    try:
        #py3
        from urllib.parse import quote
    except Exception as e:
        #py2
        from urllib import quote
    url = conf.get("url")
    upload_file_path = os.path.join(r'/tmp', name + r'.zip')
    filesize = os.path.getsize(upload_file_path)
    files = {"model": (name, open(upload_file_path, 'rb'))}
    data = {'userName': create_by, 'length': filesize, 'fileName': quote(name) + '.zip'}
    response = requests.post(url, files=files, data=data)
    if response.code == 200:
        file_path = response.json()["data"]
        return file_path
    else:
        print("status_code:{}:".format(response.code))
        sys.exit(1)


def params_file_csvtoxml(csv_name, input_type='map', xml_name='params_spec.xml'):
    """
    参数文件若为csv格式需要转化成xml
    :param csv_name: csv文件的路径
    :param input_type: 测试数据的类型，构成xml文件必要的参数
    :param xml_name: xml文件的文件名，默认值
    :return:
    """
    import pandas as pd
    df = pd.read_csv(csv_name)
    df = df.fillna("")

    header = "<?xml version='1.0' encoding='utf-8'?><params>"
    bottom = "</params>"
    inparams_begin = '<inparams type="%s">' % input_type
    inparams_end = '</inparams>'

    outparams_begin = '<outparams type="%s">' % input_type
    outparams_end = "</outparams>"

    inparam_template = "<inparam><name>%s</name><dName>%s</dName><type>%s</type><defaultValue>%s</defaultValue><datatype>%s</datatype><description>%s</description></inparam>"
    outparam_template = "<outparam><name>%s</name><dName>%s</dName><datatype>%s</datatype><description>%s</description></outparam>"

    inparam = ''
    outparam = ''
    colums = []
    for c in df.columns:
        colums.append(c.lower())
    df.columns = colums
    for index, row in df.iterrows():
        if row['params_type'] == 'input':
            inparam += (inparam_template % (
                (row["name"]), row["dname"], row['type'], row['defaultvalue'], row['datatype'], row['description']))
        else:
            outparam += (outparam_template % (row["name"], row["dname"], row['datatype'], row['description']))

    params_spec = header + inparams_begin + inparam + inparams_end + outparams_begin + outparam + outparams_end + bottom

    with open(xml_name, "w") as f:
        f.write(params_spec)


def model_build(name, handle_data=u'handle_data.py', params_file=u'params_spec.xml', model_files=[], test_data={}):
    """
    模型打包功能的总入口
    :param name: 模型名
    :param handle_data: handle_data.py的路径
    :param params_file: params_file.xml/csv文件的路径
    :param model_files: 模型相关的文件或者自定义代码文件
    :param test_data: 测试数据
    :return:
    """
    if not isinstance(model_files, list):
        raise ValueError(u"model_files 应该是一个List，eg：['path/xx.pkl','path/xx.model'] ！")
    if isinstance(test_data, list) or isinstance(test_data, dict):
        pass
    else:
        raise ValueError(u"test_data应该是一个map 或者list ！")
    try:
        params_file_path, params_file_name = os.path.split(params_file)
        params_filename, params_extension = os.path.splitext(params_file_name)
        if params_extension == u'.csv':
            if isinstance(test_data, dict):
                test_data_type = u"map"
            elif isinstance(test_data, list):
                test_data_type = u"list"
            else:
                raise ValueError(u"test_data is not map or not list!")
            params_spec_csv_file = params_file
            params_file_csvtoxml(csv_name=params_spec_csv_file, input_type=test_data_type,
                                 xml_name=os.path.join(params_file_path, u'params_spec.xml'))
            params_file = os.path.join(params_file_path, u'params_spec.xml')
            model_files.append(params_spec_csv_file)
        import sys
        sys.stdout = stdout
        sys.stderr = stderr
        print(u"1.test prepare ...\n")
        test_prepare(name, handle_data, params_file, model_files, test_data)
        sys.stdout = stdout
        sys.stderr = stderr
        print(u"1.test prepare is ok.\n")
        make_filezip(name)
        print(u"2.make zip file is ok.\n")
        storage_type = conf.get('storage_type')
        file_id = ""
        model_path = ""
        if storage_type == 'HDFS':
            model_path = upload_file_to_hdfs(name, created_by)
        else:
            file_id = upload_file(name)
            file_id = json.dumps({"hz": file_id, "stg": file_id})
        print(u"3.上传包完成\n")
        build_version = len(query_model_build_history_info(name, created_by, 'success')) + 1

        python_version_major = u"python" + str(sys.version_info.major)

        ipynbfile_path = os.getcwd()
        project_name = ipynbfile_path.split("/")[2]
        # local_project_id = query_local_project_info(project_name).id
        local_project_id = 123
        project_model_id = None
        project_model = project_model_repo.query_by_name(name, created_by)
        if project_model is not None:
            project_model_id = project_model.id
            project_model = ProjectModelDo(name=name,
                                           file_id=file_id,
                                           test_data=json.dumps(test_data),
                                           created_by=created_by,
                                           model_path=model_path,
                                           modified_by=created_by,
                                           local_project_id=local_project_id,
                                           local_project_name=project_name,
                                           build_count=build_version,
                                           model_run_env=python_version_major)
            project_model_repo.update(project_model)
            print(u"4.add model.")
            print(u"请在 机器学习平台-建模-模型包管理 中查看")
        else:

            project_model_do = ProjectModelDo()
            project_model_do.add_project_model(name=name,
                                               file_id=file_id,
                                               test_data=json.dumps(test_data),
                                               created_by=created_by,
                                               model_path=model_path,
                                               modified_by="",
                                               local_project_id=local_project_id,
                                               local_project_name=project_name,
                                               build_count=build_version,
                                               model_run_env=python_version_major)

            project_model_id = project_model_repo.add(project_model_do)
            print(u"4.add model.")
            print(u"请在 机器学习平台-建模-模型包管理 中查看")


        # if project_model is not None:
        #     project_model_id = project_model.id
        #     import ipywidgets as widgets
        #     from ipywidgets import Layout
        #     from IPython.display import display
        #
        #     debug_view = widgets.Output()
        #
        #     @debug_view.capture()
        #     def modify_button_events(b):
        #         project_model = ProjectModelDo(name=name,
        #                                        file_id=file_id,
        #                                        test_data=json.dumps(test_data),
        #                                        created_by=created_by,
        #                                        model_path=model_path,
        #                                        modified_by=created_by,
        #                                        local_project_id=local_project_id,
        #                                        local_project_name=project_name,
        #                                        build_count=build_version,
        #                                        model_run_env=python_version_major)
        #         project_model_repo.update(project_model)
        #         box_all.close()
        #         print(u"4.update model")
        #         print(u"请前往Turing-模型-“已构建模型”列表中查看")
        #
        #     @debug_view.capture()
        #     def cancel_button_events(b):
        #         box_all.close()
        #         print(u"model_build已取消")
        #
        #     style = {u'description_width': u'initial'}
        #     lable1 = widgets.Label(value=u'已构建模型列表中存在同名模型包，是否更新原模型包?', style=style, layout=Layout(width='auto'))
        #     modify_button = widgets.Button(description=u'确定', disabled=False, button_style='success',
        #                                    tooltip=u'确认将更新原模型包', icon='check', layout=Layout(width='30%'))
        #     cancel_button = widgets.Button(description=u'取消', disabled=False, button_style='warning',
        #                                    tooltip=u'取消将不会更新原模型包', icon='close', layout=Layout(width='30%'))
        #     box1 = widgets.HBox([cancel_button, modify_button])
        #     box_all = widgets.VBox([lable1, box1], layout=Layout(width='50%'))
        #     modify_button.on_click(modify_button_events)
        #     cancel_button.on_click(cancel_button_events)
        #     display(box_all)
        #     display(debug_view)
        #
        # else:
        #     # project_info = self.query_project_info()
        #     project_model_do = ProjectModelDo()
        #     project_model_do.add_project_model(name=name,
        #                                        file_id=file_id,
        #                                        test_data=json.dumps(test_data),
        #                                        created_by=created_by,
        #                                        model_path=model_path,
        #                                        modified_by="",
        #                                        local_project_id=local_project_id,
        #                                        local_project_name=project_name,
        #                                        build_count=build_version,
        #                                        model_run_env=python_version_major)
        #
        #     project_model_id = project_model_repo.add(project_model_do)
        #     print(u"4.add model.")
        #     print(u"请前往Turing-模型-“已构建模型”列表中查看")

        model_build_history_do = ModelBuildHistoryDo()
        model_build_history_do.add_model_build_history(project_model_id, u'success', build_version, name, created_by,file_id,model_path)
        model_build_history_repo = Repo()
        model_build_history_repo.add(model_build_history_do)
    except Exception as e:
        print(u'traceback.format_exc():\n%s' % traceback.format_exc())


def model_build_template():
    """
    生成模板的模型
    :return:
    """
    current_path = os.getcwd()
    if os.path.exists(os.path.join(current_path, u'model_pkg')):
        raise ValueError(u"当前目录有重名文件夹，创建模板失败")
    else:

        model_pkg_path = os.path.join(current_path, u'model_pkg')
        os.makedirs(model_pkg_path)

        shutil.copy(os.path.join(model_build_need_file_path, u'__init__.py'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'execute_model.py'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'prepare_test.py'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'handle_data.py'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'params_spec.xml'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'params_spec.csv'), model_pkg_path)
        shutil.copy(os.path.join(model_build_need_file_path, u'Python模型部署包说明文档.pdf'), model_pkg_path)
        print(u"已创建模型部署包模版，部署包内容请查看model_pkg文件夹")


if __name__ == '__main__':
    test001 = model_build('test003', 'test3/test03/params_spec.xml', 'test3/test03/handle_data.py',
                          ['test3/test03/shoujidai.xlsx', 'test3/test03/xml_type1.xlsx',
                           'test3/test03/create_xml.py'],
                          test_data={
                              "ebzz39000010": -999.0,
                              "bebz00001101": 0.0,
                              "ebzz39000011": 0.0,
                              "eazz43000011": 0.0,
                              "acbz03001011": -1111.0,
                              "abzz03132020": -999.0,
                              "abzz03132010": -999.0,
                              "ebzz35000070": -999.0,
                              "abzz03132021": 0.0,
                              "eazz28000010": -999.0,
                              "acbz03238011": -1111.0,
                              "gazz11000040": -999.0,
                              "chzz05001050": -999.0,
                              "chzz04001050": -999.0,
                              "gcaz11000011": -1111.0,
                              "chzz05138061": -1111.0,
                              "ebzz20000050": -999.0,
                              "ebzz20000051": 0.0
                          })
    test001.package()
