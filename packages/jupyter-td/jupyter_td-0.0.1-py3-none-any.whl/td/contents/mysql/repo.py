#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午10:43
# File Name: repo.py
# Description:
# ---------------------------------------------------------------------
import copy
import traceback

from mysql.connector.errors import IntegrityError
from sqlalchemy import or_
from td.contents.log.logger import log
from td.contents.mysql.db import Session
from td.contents.mysql.do import LocalProjectDo, ModelBuildHistoryDo, ProjectModelDo, JupyterResourceDo


class Repo:

    def add(self, instance, return_id=True):
        session = Session()
        result = None
        try:
            session.add(instance)
            session.commit()
            if return_id:
                result = instance.id
                return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo add error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()

    def update(self, instance):
        session = Session()
        try:
            instance_new = copy.deepcopy(instance)
            session.add(instance_new)
            session.commit()
        except BaseException as e:
            msg = traceback.format_exc()
            log.error(' repo update error. ' + msg)
            session.rollback()
            raise RepoException('repo update error.')
        finally:
            session.close()

    def batch_add(self, instances):
        session = Session()
        try:
            session.add_all(instances)
            session.commit()
        except:
            msg = traceback.format_exc()
            log.error(' repo batch_add error. ' + msg)
            session.rollback()
            raise RepoException('repo batch_add error.')
        finally:
            session.close()

    def delete(self, instance):
        session = Session()
        try:
            session.delete(instance)
            session.commit()
        except:
            msg = traceback.format_exc()
            log.error(' repo delete error. ' + msg)
            session.rollback()
            raise RepoException('repo delete error.')
        finally:
            session.close()

    def batch_delete(self, instances):
        session = Session()
        try:
            for instance in instances:
                session.delete(instance)
            session.commit()
        except:
            msg = traceback.format_exc()
            log.error(' repo batch_delete error. ' + msg)
            session.rollback()
            raise RepoException('repo batch_delete error.')
        finally:
            session.close()


class LocalProjectRepo(Repo):

    def query(self, instance, return_id=True):
        session = Session()
        result = None
        try:
            query = session.query(LocalProjectDo).filter(LocalProjectDo.name == instance.name)
            if return_id:
                result = query.one()
                return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo query error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()

    def delete(self, developer, project_name):
        session = Session()
        try:
            user1 = developer + "@tongdun.cn"
            user2 = developer + "@tongdun.net"
            session.query(LocalProjectDo).filter(or_(LocalProjectDo.developer == user1,
                                                     LocalProjectDo.developer == user2),
                                                 LocalProjectDo.name == project_name).delete()
            session.commit()
        except:
            msg = traceback.format_exc()
            log.error(' repo delete error. ' + msg)
            session.rollback()
            raise RepoException('repo delete error.')
        finally:
            session.close()

    def update(self, user, old_project_name, new_project_name):
        session = Session()
        try:
            user1 = user + "@tongdun.cn"
            user2 = user + "@tongdun.net"

            session.query(LocalProjectDo).filter(or_(LocalProjectDo.developer == user1,
                                                     LocalProjectDo.developer == user2),
                                                 LocalProjectDo.name == old_project_name).update(
                {LocalProjectDo.name: new_project_name})
            session.commit()
        except BaseException as e:
            msg = traceback.format_exc()
            log.error(' repo update error. ' + msg)
            session.rollback()
            raise RepoException('repo update error.')
        finally:
            session.close()

    def get_user_local_project_list(self, user):
        user1 = user + "@tongdun.cn"
        user2 = user + "@tongdun.net"
        session = Session()
        local_projects = session.query(LocalProjectDo).filter(or_(LocalProjectDo.developer == user1,
                                                                  LocalProjectDo.developer == user2),
                                                              LocalProjectDo.status == True).all()
        session.close()
        return local_projects


local_project_repo = LocalProjectRepo()


class ProjectModelRepo(Repo):

    def query(self, instance, return_id=True):
        session = Session()
        result = None
        try:
            query = session.query(ProjectModelDo).filter(ProjectModelDo.name == instance.name)
            if return_id:
                result = query.all()
                return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo query error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()

    def query_by_name(self, name, created_by):
        session = Session()
        result = None
        try:
            query = session.query(ProjectModelDo).filter(ProjectModelDo.name == name,
                                                         ProjectModelDo.created_by == created_by)
            result = query.first()
            return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo query error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()

    def update(self, instance):
        session = Session()
        result = None
        try:
            session.query(ProjectModelDo).filter(ProjectModelDo.name == instance.name,
                                                 ProjectModelDo.created_by == instance.created_by) \
                .update(
                {"file_id": instance.file_id, "test_data": instance.test_data, "created_by": instance.created_by,
                 "model_path": instance.model_path, "modified_by": instance.modified_by,
                 "local_project_id": instance.local_project_id, "local_project_name": instance.local_project_name,
                 "build_count": instance.build_count, "model_run_env": instance.model_run_env})
            session.commit()
        except:
            msg = traceback.format_exc()
            session.rollback()
            raise RepoException('更新模型异常,' + msg)
        finally:
            session.close()


project_model_repo = ProjectModelRepo()


class ModelBuildHistoryRepo(Repo):

    def query(self, instance, return_id=True):
        session = Session()
        result = None
        try:
            query = session.query(ModelBuildHistoryDo).filter(ModelBuildHistoryDo.created_by == instance.created_by,
                                                              ModelBuildHistoryDo.model_name == instance.model_name,
                                                              ModelBuildHistoryDo.status == instance.status)
            if return_id:
                result = query.all()
                return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo query error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()


class JupyterResourceRepo(Repo):

    def query_by_jobid_finishtime(self, job_id, pod_restart):
        session = Session()
        result = None
        try:
            query = session.query(JupyterResourceDo).filter(JupyterResourceDo.job_id == job_id,
                                                            JupyterResourceDo.pod_restart == pod_restart)
            result = query.first()
            return result
        except IntegrityError as e:
            msg = traceback.format_exc()
            log.error(' repo query error. ' + msg)
            session.rollback()
            raise RepoException('project had been in trash,please contact manager!')
        finally:
            session.close()

    def update(self, job_id, pod_restart):
        session = Session()
        try:
            session.query(JupyterResourceDo).filter(JupyterResourceDo.job_id == job_id,
                                                    JupyterResourceDo.pod_restart == 0) \
                .update({"pod_restart": pod_restart})
            session.commit()
        except:
            msg = traceback.format_exc()
            session.rollback()
            raise RepoException('更新任务结束时间异常,' + msg)
        finally:
            session.close()


if __name__ == "__main__":
    local_project = LocalProjectDo()
    # local_project.add_local_project("project_name_1","zhangsan")
    # local_project_repo.add(local_project)
    # project_model = ProjectModelDo(name="test009",file_id="s0-8e3d1860-0e72-11e9-987c-f9bcd5707d93",
    #                                 test_data="{'eazz28000010': -999.0, 'acbz03001011': -1111.0, 'chzz05138061': -1111.0, 'bebz00001101': 0.0, 'ebzz20000051': 0.0, 'chzz05001050': -999.0, 'ebzz35000070': -999.0, 'abzz03132010': -999.0, 'ebzz20000050': -999.0, 'gazz11000040': -999.0, 'eazz43000011': 0.0, 'abzz03132020': -999.0, 'abzz03132021': 0.0, 'ebzz39000010': -999.0, 'ebzz39000011': 0.0, 'acbz03238011': -1111.0, 'gcaz11000011': -1111.0, 'chzz04001050': -999.0}",
    #                                 created_by="qiaoshi.wang@tongdun.net",build_count=53)
    #
    # project_model_repo.update(project_model)
    # print(project_model_repo.query_by_name("dbsh","dsfdsf"))

    #
    #
    # old_local_project = LocalProjectDo()
    # old_local_project.add_local_project("project_name_2","zhangsan")
    # local_project_repo.add(old_local_project)
    #
    # new_local_project = LocalProjectDo()
    # new_local_project.add_local_project("project_name_new", "zhangsan")

    # local_project_repo.update("zhangsan","project_name_1","project_name_new")

    # local_projects = local_project_repo.get_user_local_project_list("zhangsan")

    # local_project_repo.delete("zhangsan","project_name_new")

    # for project in local_projects:
    #     print(project.name)


class RepoException(Exception):
    """
    异常
    """
    pass
