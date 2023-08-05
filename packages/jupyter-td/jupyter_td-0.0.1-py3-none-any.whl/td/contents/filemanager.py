#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/2 上午9:24
# File Name: filemanager.py
# Description:
# ---------------------------------------------------------------------
from notebook.services.contents.largefilemanager import LargeFileManager
from tornado import web
from send2trash import send2trash
import sys,os,shutil


class TDFileContentsManager(LargeFileManager):
    def delete_file(self, path):
        """Delete file at path."""
        path = path.strip('/')
        os_path = self._get_os_path(path)
        rm = os.unlink
        if not os.path.exists(os_path):
            raise web.HTTPError(404, u'File or directory does not exist: %s' % os_path)

        def _check_trash(os_path):
            return True
            # if sys.platform in {'win32', 'darwin'}:
            #     return True
            #
            # # It's a bit more nuanced than this, but until we can better
            # # distinguish errors from send2trash, assume that we can only trash
            # # files on the same partition as the home directory.
            # file_dev = os.stat(os_path).st_dev
            # home_dev = os.stat(os.path.expanduser('~')).st_dev
            # return file_dev == home_dev

        def is_non_empty_dir(os_path):
            if os.path.isdir(os_path):
                # A directory containing only leftover checkpoints is
                # considered empty.
                cp_dir = getattr(self.checkpoints, 'checkpoint_dir', None)
                if set(os.listdir(os_path)) - {cp_dir}:
                    return True

            return False

        if self.delete_to_trash:
            if sys.platform == 'win32' and is_non_empty_dir(os_path):
                # send2trash can really delete files on Windows, so disallow
                # deleting non-empty files. See Github issue 3631.
                raise web.HTTPError(400, u'Directory %s not empty' % os_path)
            if _check_trash(os_path):
                self.log.debug("Sending %s to trash", os_path)
                # Looking at the code in send2trash, I don't think the errors it
                # raises let us distinguish permission errors from other errors in
                # code. So for now, just let them all get logged as server errors.
                send2trash(os_path)
                return
            else:
                self.log.warning("Skipping trash for %s, on different device "
                                 "to home directory", os_path)
        if os.path.isdir(os_path):
            # Don't permanently delete non-empty directories.
            if is_non_empty_dir(os_path):
                raise web.HTTPError(400, u'Directory %s not empty' % os_path)
            self.log.debug("Removing directory %s", os_path)
            with self.perm_to_403():
                shutil.rmtree(os_path)
        else:
            self.log.debug("Unlinking file %s", os_path)
            with self.perm_to_403():
                rm(os_path)

    # def get_user_name(self):
    #     try:
    #         return conf.get_user_name()
    #     except Exception as e:
    #         raise HTTPError(500, reason=e)
    #
    # def new_untitled(self, path='', type='', ext=''):
    #     if path == '/' and type != 'directory':
    #         raise HTTPError(400, reason="cannot create file in / directory")
    #     return super(TDFileContentsManager,self).new_untitled(path,type,ext)
    #
    # def new_project(self,model,path):
    #     path = path.strip('/')
    #     os_path = self._get_os_path(path)
    #     if os.path.exists(os_path):
    #         raise HTTPError(500, log_message="Project already existed, change the name!",reason="Project already existed, change the name!")
    #
    #     model = self.new(model, path)
    #
    #     user_name = self.get_user_name()
    #
    #     #注 册 信 息至mysql中
    #     try:
    #         local_project_do = LocalProjectDo()
    #         local_project_do.add_local_project(path,user_name)
    #
    #         local_project_repo.add(local_project_do)
    #     except:
    #         self.delete(path)
    #         raise HTTPError(500, reason="Project already existed, change the name!")
    #
    #     #在文件目录中创建文件
    #     return model
    #
    # def new_project_tlib(self,model,path):
    #     path = path.strip('/')
    #     os_path = self._get_os_path(path)
    #     print(os_path);
    #     if os.path.exists(os_path):
    #         print("model exist!!!")
    #         return False;
    #     model = self.new(model, path)
    #     # todo: 这里有问题
    #     user_name = self.get_user_name()
    #     print("path:" + path)
    #     print("os_path:" + os_path)
    #     print("user_name:" + user_name)
    #
    #     #注 册 信 息至mysql中
    #     try:
    #         local_project_do = LocalProjectDo()
    #         local_project_do.add_local_project(path,user_name)
    #         local_project_repo.add(local_project_do)
    #     except:
    #         self.delete(path)
    #         raise HTTPError(500, reason="Project already existed, change the name!")
    #
    #     #在文件目录中创建文件
    #     return model
    #
    # def update_local_project(self,model,path):
    #     path = path.strip('/')
    #
    #     model = self.update(model,path)
    #     new_name = model['name']
    #
    #     user_name = self.get_user_name().replace("@tongdun.cn","").replace("@tongdun.net","")
    #     try:
    #         local_project_repo.update(user_name,path,new_name)
    #     except:
    #         model['name'] = path
    #         self.update(model,new_name)
    #         raise HTTPError(500,reason="update failed,please retry")
    #
    #     return model
    #
    # def del_local_project(self,path):
    #     path = path.strip('/')
    #
    #     user_name = self.get_user_name().replace("@tongdun.cn","").replace("@tongdun.net","")
    #     #先修改数据库
    #     local_project_repo.delete(user_name,path)
    #     self.delete(path)
    #
    # def list_local_project(self):
    #     user_name = self.get_user_name().replace("@tongdun.cn","").replace("@tongdun.net","")
    #     local_projects = local_project_repo.get_user_local_project_list(user_name)
    #
    #     model = self._base_model("")
    #     model['format']='json'
    #     model['type'] = 'directory'
    #     model['size'] = None
    #     model['content'] = contents = []
    #     for local_project in local_projects:
    #         if self.exists(local_project.name):
    #             m = self._base_model(local_project.name)
    #             m['format'] = 'json'
    #             m['type'] = 'directory'
    #             m['size'] = None
    #             m['content'] = None
    #             contents.append(m)
    #     # 添加notebook使用文档
    #     if self.exists("notebook使用文档"):
    #         m = self._base_model('notebook使用文档')
    #         m['format'] = 'json'
    #         m['type'] = 'directory'
    #         m['size'] = None
    #         m['content'] = None
    #         contents.append(m)
    #
    #     if self.exists("notebook常见问题"):
    #         m = self._base_model('notebook常见问题')
    #         m['format'] = 'json'
    #         m['type'] = 'directory'
    #         m['size'] = None
    #         m['content'] = None
    #         contents.append(m)
    #
    #     if self.exists(tensorboard_logdir+"/"+user_name):
    #         m = self._base_model(tensorboard_logdir)
    #         m['format'] = 'json'
    #         m['type'] = 'directory'
    #         m['size'] = None
    #         m['content'] = None
    #         contents.append(m)
    #
    #     return model
    #
    # def list_tensorboardlogs(self):
    #     user_name = self.get_user_name().replace("@tongdun.cn","").replace("@tongdun.net","")
    #     model = self._base_model(tensorboard_logdir)
    #     model['format'] = 'json'
    #     model['type'] = 'directory'
    #     model['size'] = None
    #     model['content'] = contents = []
    #
    #     m = self._base_model(tensorboard_logdir+"/"+user_name)
    #     m['format'] = 'json'
    #     m['type'] = 'directory'
    #     m['size'] = None
    #     m['content'] = None
    #     contents.append(m)
    #
    #     return model







