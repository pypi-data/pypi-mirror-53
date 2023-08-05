#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 18/8/14 下午5:02
# File Name: db.py
# Description:
# ---------------------------------------------------------------------
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from td.contents.util.config import conf
import functools

engine = None
Session = None


def create_mysql_engine():
    # 初始化数据库连接:
    engine_args = {}
    sql_alchemy_conn = conf.get('sql_alchemy_conn')
    engine_args['pool_size'] = conf.getint('sql_alchemy_pool_size')
    engine_args['pool_recycle'] = conf.getint('sql_alchemy_pool_recycle')

    global engine
    global Session
    engine = create_engine(sql_alchemy_conn, encoding='utf-8', convert_unicode=True, **engine_args)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)



create_mysql_engine()


class _TransactionCtx(object):
    def __init__(self, session=None):
        self.session = session

    def __enter__(self):
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if exctype is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()


def with_transaction(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        global Session
        session = Session()
        kwargs['session'] = session
        with _TransactionCtx(session=session):
            return func(*args, **kwargs)

    return _wrapper
