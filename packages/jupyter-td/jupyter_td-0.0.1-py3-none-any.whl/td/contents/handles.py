#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/7/4 下午4:47
# File Name: handles.py
# Description:
# ---------------------------------------------------------------------
from notebook.services.sessions.handlers import SessionRootHandler, SessionHandler,APIHandler
from notebook.utils import url_path_join
from notebook.services.contents.handlers import ContentsHandler, validate_model, CheckpointsHandler
from notebook.base.handlers import (
    IPythonHandler, path_regex,
)
from tornado import gen, web
from tornado.web import URLSpec, RequestHandler
import json, os, shutil
import requests

from .conf.constants import (dfs_url,tlib_nb_path)

from td.contents.util.config import conf,tensorboard_logdir
user_name = conf.get_user_name()
enki_url = conf.get("enki_url")

# 添加新功能
class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('ok')


sparkmagic_session_ids = []

templates = [{"module":"基础案列","notebooks":["gbdt_demo1.ipynb","xgboost_demo1.ipynb"]},
             {"module":"自动化案列","notebooks":["AutoML-Example01-Inner-behavior.ipynb",
                                                "AutoML-Example02-Register.ipynb"]}]


class TlibUrlHandler(APIHandler):
    @gen.coroutine
    def get(self):
        result = {"status": 0, "success": True, "message": "", "data": enki_url}
        return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass


class TlibENVQuery(APIHandler):
    @gen.coroutine
    def get(self):
        r = requests.get("%s/algo/envQuery" % enki_url, timeout=10)
        if r.status_code == 200:
            return self.finish(json.dumps(r.json()))
        else:
            result = {"status": 1, "success": False, "message": "网络问题"}
            return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass


class TlibListQuery(APIHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        headers = {"Content-Type": "application/json"}
        data = self.get_json_body()
        r = requests.post("%s/algo/listQuery" % enki_url, data=json.dumps(data), headers=headers, timeout=10)
        if r.status_code==200:
            return self.finish(json.dumps(r.json()))
        else:
            result = {"status": 1, "success": False, "message": "网络问题"}
            return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass


class CloneTemplateHandler(ContentsHandler):
    @gen.coroutine
    def post(self):
        status = 0
        success = True
        message = "克隆成功"
        root_dir = self.contents_manager.root_dir
        model = self.get_json_body()
        source = model['source']
        dest = model['dest']

        source_path = os.path.abspath(os.path.dirname(__file__)) + "/template/" + source['notebook']
        dest_path = root_dir + "/" + dest["project"]

        if not os.path.exists(source_path):
            message = source['notebook'] + "案列不存在"
            success = False
            status = 1
        elif not os.path.exists(dest_path):
            success = False
            status = 1
            message = dest["project"] + "工程不存在"
        else:
            shutil.copyfile(source_path, dest_path + "/" + dest['notebook'])
        result = {"status": status, "success": success, "message": message}
        return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass


class TemplateHandler(ContentsHandler):
    @gen.coroutine
    def get(self):
        result = {"status":0,"success":True,"data":templates}
        self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass

import subprocess
class CloneRemoteProjectHandler(APIHandler):
    def clone(self):
        pass

    @gen.coroutine
    def post(self):
        root_dir = self.contents_manager.root_dir
        data = self.get_json_body()
        gitUrl = data['gitUrl']
        localProjectName = data['localProjectName']
        p = subprocess.Popen(["git", "clone",gitUrl,localProjectName], cwd=root_dir,stdout = subprocess.PIPE,stderr=subprocess.PIPE)
        code = p.wait()
        if code!=0:
            result = {"status": 1, "success": False, "message": str(p.stderr.read())}
        else:
            result = {"status": 0, "success": True, "message": "克隆成功"}
        return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass


class ListRemoteProjectHandler(APIHandler):

    def getFromTruing(self):
        pass

    @gen.coroutine
    def get(self):
        result = {}
        if enki_url != None:
            list_project_url = enki_url + "/jupyter/project/listV2?curPage=1&pageSize=1000&userName="+user_name
            r = requests.get(list_project_url, timeout=5)
            if r.status_code == 200:
                result = r.json()
        else:
            result = {"status": 1, "success": False, "message": "turing地址获取不到!", "data": []}
        print(result)
        return self.finish(json.dumps(result))

    def check_xsrf_cookie(self):
        pass

class LocalProjectHandler(APIHandler):
    @gen.coroutine
    def get(self):
        root_dir = self.contents_manager.root_dir
        root_dir_list = os.listdir(root_dir)

        data = []
        result = {"status": 0, "success": True, "message": "本地项目列表", "data": data}
        for item in root_dir_list:
            if os.path.isdir(root_dir + "/" + item):
                data.append({
                             "name": item,
                             "git_url": "https://github.com/dask/distributed.git"
                             })
        return self.finish(json.dumps(result))
    def check_xsrf_cookie(self):
        pass


class SparkMagicSessionHandler(APIHandler):
    def get(self):
        self.finish(json.dumps(sparkmagic_session_ids))

    def delete(self):
        id = int(self.get_argument("id"))
        for i in range(len(sparkmagic_session_ids)):
            if id == sparkmagic_session_ids[i]:
                sparkmagic_session_ids.remove(i)

    def post(self):
        id = int(self.get_argument("id"))
        sparkmagic_session_ids.append(id)

    def check_xsrf_cookie(self):
        pass
# 上传文件
class UploadFileHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    @gen.coroutine
    def post(self):
        print("change")
        path = ""
        if self.get_argument('path', '/usr') != "/usr":
            path = self.get_argument('path', '/usr')
        else:
            raise web.HTTPError(500, reason="缺少path参数")
        if self.request.files:
            for meta in self.request.files.get('file', None):
                filename = meta['filename']
                file_path = os.path.join(path, filename);
                with open(file_path, 'wb') as up:
                    up.write(meta['body'])
        self.finish('ok')

    def check_xsrf_cookie(self):
        pass


# 上传文件
class GetNotebook4TlibHandler(ContentsHandler):
    def data_received(self, chunk):
        pass

    @gen.coroutine
    def get(self):
        if self.get_argument('fileId', '*') != "*":
            file_id = self.get_argument('fileId', '/usr')
            file_name = self.get_argument('fileName', '/usr')
            domain_name = self.get_argument('domainName', '/usr')
            self.log.info("file_id:"+file_id+" file_name:"+file_name+" domain_name:"+domain_name);
        else:
            raise web.HTTPError(500, reason="缺少fileId参数")

        if file_name == "":
            self.finish('not ok')
        path = tlib_nb_path+"_"+domain_name;

        model = {"ext": path, "path": "", "type": "directory"}
        path = "/" + model['ext'][0:]
        model = self.contents_manager.new_project_tlib(model, path);
        self.log.info("path:"+path);

        if self.dfs_download(file_id, "/notebooks"+path+"/"+file_name):
            self.finish('ok')
        else:
            self.finish('not ok')

    def check_xsrf_cookie(self):
        pass

    def dfs_download(self, algo_file_id, file_name):

        r = requests.get("%s/rest/api/%s" % (dfs_url, algo_file_id), timeout=5)
        if r.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(r.content)
            return True
        return False


# 覆盖原功能,ContentsHandler是展现,编写,刷新等(文件,目录)
class TDContentsHandler(ContentsHandler):

    @gen.coroutine
    def post(self, path=''):
        model = self.get_json_body()
        if model.get("type") is not None and model['type'] == 'directory' and (path == '/' or path == ''):
            path = "/" + model['ext'][1:]
            model['ext'] = ''
            model = self.contents_manager.new_project(model, path)
            self.log.info(u"Creating new project  %s", path)
            model = yield gen.maybe_future(model)
            self.set_status(201)
            validate_model(model, expect_content=False)
            self._finish_model(model)
        elif model.get("type") is not None and model['type'] != 'directory' and (path == '/' or path == ''):
            self.set_header("Content-Type", "application/json;charset=utf-8")
            raise web.HTTPError(400, reason=u"   <<Cannot make file or notebook in /,please select one of dirs>>",
                                log_message="根目录不支持新建文件，请先创建工程文件夹!")
        else:
            super(TDContentsHandler, self).post(path)

    @web.authenticated
    @gen.coroutine
    def put(self, path=''):
        model = self.get_json_body()
        if model['type'] == 'directory' and (path == '/' or path == ''):
            model = self.contents_manager.new_project(model, path)
            self.set_status(201)
            validate_model(model, expect_content=False)
            self._finish_model(model)
        elif model['type'] == 'file' and len(path.split("/")) == 2:
            # self.set_status(500)
            # self.set_header("Content-Type","application/json;charset=utf-8")
            # self.finish(json.dumps(
            #     dict(message="spark最多开启了4个!", traceback="spark最多开启了4个!", short_message="spark最多开启了4个!", status=201,
            #          statusText="python单机最多开启4个!",reason="根目录不支持上传文件,请先创建工程文件夹!",log_message="根目录不支持上传文件,请先创建工程文件夹!")))
            raise web.HTTPError(400, reason="can not upload file in root directory,please mkdir  directory first!",
                                log_message="can not upload file in root directory,please mkdir  directory first!")
        else:
            super(TDContentsHandler, self).put(path)

    @web.authenticated
    @gen.coroutine
    def patch(self, path=''):
        model = self.get_json_body()
        path_tmp = path.strip('/')
        if "/" not in path_tmp:
            ##更新注册信息
            model = self.contents_manager.update_local_project(model, path)
            validate_model(model, expect_content=False)
            self._finish_model(model)
        else:
            super(TDContentsHandler, self).patch(path)

    @web.authenticated
    @gen.coroutine
    def delete(self, path=''):
        """delete a file in the given path"""
        path_tmp = path.strip('/')
        if path_tmp.startswith(tensorboard_logdir):
            raise web.HTTPError(400, reason="tensorboard_logdir不能删")
        if "/" not in path_tmp:
            self.contents_manager.del_local_project(path)
            self.set_status(204)
            self.finish()

        else:
            super(TDContentsHandler, self).delete(path)

    @web.authenticated
    @gen.coroutine
    def get(self, path=''):
        if path == "" or path == "/":
            model = self.contents_manager.list_local_project()
            self._finish_model(model, location=False)
        elif path == "/"+tensorboard_logdir:
            model = self.contents_manager.list_tensorboardlogs()
            self._finish_model(model, location=False)
        else:
            super(TDContentsHandler, self).get(path)

    # @web.authenticated
    # @gen.coroutine
    # def get(self, path=''):
    #
    #     """Return a model for a file or directory.
    #
    #            A directory model contains a list of models (without content)
    #            of the files and directories it contains.
    #            """
    #     path = path or ''
    #     type = self.get_query_argument('type', default=None)
    #     if type not in {None, 'directory', 'file', 'notebook'}:
    #         raise web.HTTPError(400, u'Type %r is invalid' % type)
    #
    #     format = self.get_query_argument('format', default=None)
    #     if format not in {None, 'text', 'base64'}:
    #         raise web.HTTPError(400, u'Format %r is invalid' % format)
    #     content = self.get_query_argument('content', default='1')
    #     if content not in {'0', '1'}:
    #         raise web.HTTPError(400, u'Content %r is invalid' % content)
    #     content = int(content)
    #
    #     model = yield gen.maybe_future(self.contents_manager.get(
    #         path=path, type=type, format=format, content=content,
    #     ))
    #     validate_model(model, expect_content=content)
    #
    #
    #
    #     c = filter(lambda item:item['name'].startswith(u"b"), model['content'])
    #     model['content'] = c
    #     self._finish_model(model, location=False)


class TDSessionHandler(SessionRootHandler):

    @web.authenticated
    @gen.coroutine
    def post(self):
        model = self.get_json_body()
        kernel = model.get('kernel', {})
        kernel_name = kernel.get('name', None)

        sm = self.session_manager
        python_count = 0
        spark_count = 0
        for session in sm.list_sessions():
            kn = session['kernel'].get("name").lower()
            if "python" in kn:
                python_count += 1
            elif "spark" in kn:
                spark_count += 1
        #todo: python资源限制

        if "python" in kernel_name and python_count >= 10:
            self.set_status(500)
            self.finish(json.dumps(
                dict(message="python单机最多开启10个!", traceback="python单机最多开启10个!", short_message="python单机最多开启10个!",
                     status=201, statusText="python单机最多开启10个!")))
            return

        # mem_info = get_os_mem()
        # mem_used = mem_info["used"]
        # mem_total = mem_info["total"]
        # mem_threshold = mem_total /100 * 90
        #
        # if "python" in kernel_name and mem_used > mem_threshold:
        #     self.set_status(500)
        #     self.finish(json.dumps(
        #         dict(message="系统资源不足!", traceback="系统资源不足!", short_message="系统资源不足!",
        #              status=201, statusText="系统资源不足!")))
        #     return

        if "spark" in kernel_name and spark_count >= 4:
            self.log.warning('Kernel not found: %s' % kernel_name)
            self.set_status(500)
            self.finish(json.dumps(
                dict(message="spark最多开启4个!", traceback="spark最多开启4个!", short_message="spark最多开启4个!", status=201,
                     statusText="spark最多开启4个!")))
            return

        return super(TDSessionHandler, self).post()


# 用于变更jupyter路由
def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    nb_server_app.log.info("load td extension")

    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/ok')
    web_app.add_handlers(host_pattern, [(route_pattern, HelloWorldHandler)])

    handlers = web_app.wildcard_router.rules

    # pattern = url_path_join(web_app.settings['base_url'], r"/api/contents%s" % path_regex)
    # new_handler = URLSpec(pattern, TDContentsHandler)
    # handlers.insert(0, new_handler)

    _session_id_regex = r"(?P<session_id>\w+-\w+-\w+-\w+-\w+)"

    session_pattern = url_path_join(web_app.settings['base_url'], r"/api/sessions/%s" % _session_id_regex)
    session_handler = URLSpec(session_pattern, SessionHandler)
    handlers.insert(0, session_handler)

    session_root_pattern = url_path_join(web_app.settings['base_url'], r"/api/sessions")
    session_root_handler = URLSpec(session_root_pattern, TDSessionHandler)
    handlers.insert(0, session_root_handler)

    upload_route_pattern = url_path_join(web_app.settings['base_url'], r'/upload')
    upload_handler = URLSpec(upload_route_pattern, UploadFileHandler)
    handlers.insert(0, upload_handler)

    get_notebook4tlib_handler_pattern = url_path_join(web_app.settings['base_url'], r'/getNotebook4Tlib')
    get_notebook4tlib_handler = URLSpec(get_notebook4tlib_handler_pattern, GetNotebook4TlibHandler)
    handlers.insert(0, get_notebook4tlib_handler)


    sparkmagic_session_handler_pattern = url_path_join(web_app.settings['base_url'], r'/sparkmagic/session')
    sparkmagic_session_handler = URLSpec(sparkmagic_session_handler_pattern, SparkMagicSessionHandler)
    handlers.insert(0, sparkmagic_session_handler)

    template_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/template/list')
    template_handler = URLSpec(template_handler_pattern, TemplateHandler)
    handlers.insert(0, template_handler)

    clone_template_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/template/clone')
    clone_template_handler = URLSpec(clone_template_handler_pattern, CloneTemplateHandler)
    handlers.insert(0, clone_template_handler)

    remote_project_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/remoteProject/list')
    remote_project_handler = URLSpec(remote_project_handler_pattern, ListRemoteProjectHandler)
    handlers.insert(0, remote_project_handler)

    clone_remote_project_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/remoteProject/clone')
    clone_remote_project_handler = URLSpec(clone_remote_project_handler_pattern, CloneRemoteProjectHandler)
    handlers.insert(0, clone_remote_project_handler)

    local_project_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/localProject/list')
    local_project_handler = URLSpec(local_project_handler_pattern, LocalProjectHandler)
    handlers.insert(0, local_project_handler)

    tlib_url_handler_pattern = url_path_join(web_app.settings['base_url'], r'/api/apiUrl')
    tlib_url_handler = URLSpec(tlib_url_handler_pattern, TlibUrlHandler)
    handlers.insert(0, tlib_url_handler)

    tlib_list_handler_pattern = url_path_join(web_app.settings['base_url'], r'/algo/listQuery')
    tlib_list_handler = URLSpec(tlib_list_handler_pattern, TlibListQuery)
    handlers.insert(0, tlib_list_handler)

    tlib_env_handler_pattern = url_path_join(web_app.settings['base_url'], r'/algo/envQuery')
    tlib_env_handler = URLSpec(tlib_env_handler_pattern, TlibENVQuery)
    handlers.insert(0, tlib_env_handler)