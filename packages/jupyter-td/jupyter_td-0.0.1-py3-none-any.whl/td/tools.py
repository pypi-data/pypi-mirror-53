#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2018/11/26 下午7:27
# File Name: tools.py
# Description:
# ---------------------------------------------------------------------
def int_type(num):
    na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', 'N/A', 'NA',
                 'NULL', 'NaN', 'n/a', 'nan', 'null']
    if num in na_values:
        raise Exception("不能存在NA值")
    if num >= 0 and num <= 255:
        return "uint8"
    elif num >= 0 and num <= 65535:
        return "uint16"
    elif num >= 0 and num <= 4294967295:
        return "uint32"
    elif num >= 0 and num <= 18446744073709551615:
        return "uint64"
    elif num >= -128 and num <= 127:
        return "int8"
    elif num >= -32768 and num <= 32767:
        return "int16"
    elif num >= -2147483648 and num <= 2147483647:
        return "int32"
    elif num >= -9223372036854775808 and num <= 9223372036854775807:
        return "int64"


def set_int_type(num, dtype):
    int_priority = {"uint8": 1, "uint16": 2, "uint32": 3, "uint64": 4, "int8": 5, "int16": 5, "int32": 6, "int64": 7}
    now_type = int_type(num)
    if int_priority[now_type] > int_priority[dtype]:
        return now_type
    else:
        return dtype


def float_type(num):
    na_values = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', 'N/A', 'NA',
                 'NULL', 'NaN', 'n/a', 'nan', 'null']
    if num in na_values:
        raise Exception("不能存在NA值")
    if num >= -65537 and num <= 65536:
        return "float16"
    else:
        return "float32"


def set_float_type(num, dtype):
    float_priority = {"float16": 1, "float32": 2}
    now_type = float_type(num)
    if float_priority[now_type] > float_priority[dtype]:
        return now_type
    else:
        return dtype


def recommend_dtypes(f):
    import pandas as pd
    import io
    import sys
    file_name = None

    if sys.version.split("|")[0] > "3":
        if isinstance(f, io.TextIOWrapper) or isinstance(f, io.BufferedWriter):
            file_name = f.name
        elif isinstance(f, str):
            file_name = f
        else:
            raise Exception("参数必须为file对像或者文件名")

    elif sys.version.split("|")[0] < "3":
        if isinstance(f, file):
            file_name = f.name
        elif isinstance(f, str):
            file_name = f
        else:
            raise Exception("参数必须为file对像或者文件名")

    df = pd.read_csv(file_name,nrows = 10000)
    dtypes = {}
    category = []
    result = {}
    length = len(df.dtypes)
    for i in range(0, length):
        dtype = df.dtypes[i]
        name = df.columns[i]
        if dtype == "int":
            dtypes[i+1] = {"type":"uint8","name":name}
        elif dtype == "float":
            dtypes[i+1] = {"type":"float16","name":name}
        else:
            category.append(name)

    for row in df.itertuples():
        for key, value in dtypes.items():
            num = row[key]
            now_type = value['type']
            name = value['name']
            if "int" in value:
                now_type = set_int_type(num, now_type)
            elif "float" in value:
                now_type = set_float_type(num, now_type)
            dtypes[key] = {"type":now_type,"name":name}

    for key, value in dtypes.items():
        now_type = value['type']
        name = value['name']
        result[name] = now_type
    df = None
    dtypes = None
    print("列[" + ",".join(category) + "],如果是范围值,请使用category,将有效降低dataframe内存")
    return result


def memory_usage():
    import psutil
    import os
    use_memory = round(psutil.Process(os.getpid()).memory_info().rss / 1048576, 2)
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        spark_d_total_memory = spark.sparkContext.getConf().get("spark.driver.memory", '0')
        spark_d_total_memory = spark_d_total_memory.lower()
    except:
        python_total_memory = 61440
        used_ratio = round(use_memory * 100 / python_total_memory, 2)
        used_ratio_str = "%0.2f%%" % used_ratio
        print("kernel总内存:{}M     kernel已用内存:{}M       内存利用率{}".format(python_total_memory,use_memory,used_ratio_str))
        return

    if "g" in spark_d_total_memory:
        spark_d_total_memory = int(spark_d_total_memory.replace("g", ""))*1024
        used_ratio = round(use_memory * 100 / spark_d_total_memory, 2)
        used_ratio_str = "%0.2f%%" % used_ratio
        print("kernel总内存:{}M     kernel已用内存:{}M       内存利用率{}".format(spark_d_total_memory,use_memory,used_ratio_str))
        return
    elif "m" in spark_d_total_memory:
        spark_d_total_memory = int(spark_d_total_memory.replace("m", ""))
        used_ratio = round(use_memory * 100 / spark_d_total_memory, 2)
        used_ratio_str = "%0.2f%%" % used_ratio
        print("kernel总内存:{}M     kernel已用内存:{}M       内存利用率{}".format(spark_d_total_memory, use_memory, used_ratio_str))
        return
    else:
        print("无法获取spark.driver.memory的配置信息，请使用%configure_gui配置spark.driver.memory的大小.")

