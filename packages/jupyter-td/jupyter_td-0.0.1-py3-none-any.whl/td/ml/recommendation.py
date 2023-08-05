#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2019/1/15 下午2:42
# File Name: recommendation.py
# Description:
# ---------------------------------------------------------------------
class TDALSModel(object):

    def __init__(self, model,
                 src_block_Size,
                 dst_block_size,
                 is_user_small,
                 is_item_small,
                 en_ratio, user_partition_num, item_partition_num):
        self.model = model
        self.src_block_Size = src_block_Size
        self.dst_block_size = dst_block_size
        self.is_user_small = is_user_small
        self.is_item_small = is_item_small
        self.en_ratio = en_ratio
        from pyspark.sql import SparkSession
        self.spark = SparkSession.builder.getOrCreate()
        self.jvm = self.spark.sparkContext._jvm
        self.sql_ctx = self.spark._wrapped
        self.td_alsmodel_obj = self.jvm.org.apache.spark.ml.recommendation.TDALSModel.load(model._java_obj,
                                                                                           self.src_block_Size,
                                                                                           self.dst_block_size,
                                                                                           self.is_user_small,
                                                                                           self.is_item_small,
                                                                                           self.en_ratio,
                                                                                           user_partition_num,
                                                                                           item_partition_num)

    @staticmethod
    def load(model,
             src_block_Size=4096,
             dst_block_size=4096,
             is_user_small=False,
             is_item_small=True,
             en_ratio=True,
             user_partition_num=0,
             item_partition_num=0):
        td_als_model = TDALSModel(model, src_block_Size, dst_block_size,
                                  is_user_small, is_item_small, en_ratio, user_partition_num, item_partition_num)
        return td_als_model

    def recommendForAllItems(self, num_users):
        df_obj = self.td_alsmodel_obj.recommendForAllItems(num_users)
        from pyspark.sql import DataFrame
        return DataFrame(df_obj, self.sql_ctx)

    def recommendForAllUsers(self, num_items):
        df_obj = self.td_alsmodel_obj.recommendForAllUsers(num_items)
        from pyspark.sql import DataFrame
        return DataFrame(df_obj, self.sql_ctx)
