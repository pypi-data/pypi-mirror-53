#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午10:31
# File Name: do.py
# Description:
# ---------------------------------------------------------------------
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class LocalProjectDo(Base):
    __tablename__ = 't_local_project'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    developer = Column(String(64))
    status = Column(Boolean, default=True)

    def add_local_project(self, name, developer):
        self.name = name
        self.developer = developer

    def query_local_project(self, name):
        self.name = name


class ProjectModelDo(Base):
    __tablename__ = 't_project_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    label = Column(String(256))
    detail = Column(String(1024))
    file_id = Column(String(256))
    extend_field = Column(String(256))
    created_by = Column(String(64), default="")
    modified_by = Column(String(64), default="")
    gmt_create = Column(TIMESTAMP, server_default=func.now())
    gmt_modify = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    project_id = Column(Integer)
    test_data = Column(String)
    git_url = Column(String(128))
    dag_id = Column(Integer)
    partner_code = Column(String(45))
    build_count = Column(Integer)
    last_build_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deploy_status = Column(String(45))
    deploy_detail = Column(String(256))
    deploy_env = Column(String(45))
    deploy_status_update_time = Column(String)
    deploy_count = Column(Integer)
    mid = Column(String(64))
    sandbox_mid = Column(String(64))
    model_run_env = Column(String(50))
    local_project_id = Column(Integer)
    local_project_name = Column(String(128))
    model_path = Column(String)

    def add_project_model(self, name, file_id, test_data, created_by, model_path, modified_by, local_project_id, local_project_name, build_count,
                          model_run_env):
        self.name = name
        self.file_id = file_id
        self.test_data = test_data
        self.created_by = created_by
        self.model_path = model_path
        self.modified_by = modified_by
        self.local_project_id = local_project_id
        self.local_project_name = local_project_name
        self.build_count = build_count
        self.model_run_env = model_run_env


class ModelBuildHistoryDo(Base):
    __tablename__ = 't_model_build_history'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer)
    project_type = Column(Integer)
    dag_id = Column(Integer)
    dag_name = Column(String(64))
    status = Column(String(45))
    version = Column(Integer)
    model_name = Column(String(32))
    created_by = Column(String(64))
    file_id = Column(String(256))
    model_path = Column(String(256))

    def add_model_build_history(self, model_id, status, version, model_name, created_by,file_id,model_path):
        self.model_id = model_id
        self.status = status
        self.version = version
        self.model_name = model_name
        self.created_by = created_by
        self.file_id = file_id
        self.model_path = model_path

    def query_model_build_history(self, model_name, created_by, status):
        self.model_name = model_name
        self.created_by = created_by
        self.status = status


class JupyterResourceDo(Base):
    __tablename__ = 't_jupyter_resource'
    id = Column(Integer, primary_key=True)
    job_id = Column(String(32))
    job_name = Column(String(64))
    job_type = Column(Integer)
    user_id = Column(String(32))
    user_name = Column(String(32))
    pod_name = Column(String(64))
    pod_restart = Column(Integer)
    gpu_uuid = Column(String(32))
    gpu_num = Column(Integer)

    def add_jupyter_resource(self, job_id, job_name, job_type, user_id, user_name, pod_name, pod_restart, gpu_uuid,
                             gpu_num):
        self.job_id = job_id
        self.job_name = job_name
        self.job_type = job_type
        self.user_id = user_id
        self.user_name = user_name
        self.pod_name = pod_name
        self.pod_restart = pod_restart
        self.gpu_uuid = gpu_uuid
        self.gpu_num = gpu_num
