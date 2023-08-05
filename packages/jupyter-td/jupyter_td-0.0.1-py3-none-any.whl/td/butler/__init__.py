#!/usr/bin/env python
# coding=utf-8
# ------------------------------------------------------------------------
# Author: wqs
# Created Time: 2018/11/26 下午7:27
# File Name: __init__.py
# Description:
# ---------------------------------------------------------------------

import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType,StringType,LongType

from petastorm.codecs import ScalarCodec, CompressedImageCodec, NdarrayCodec
from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField


hive_base_url = "hdfs://tdhdfs-cs-hz/user/hive/warehouse/"
user_name = "qiaoshi.wang"


def set_env():
    import os
    import subprocess
    user_name = os.environ['user_name']
    os.environ['HADOOP_PROXY_USER'] = user_name
    os.system("kinit -kt dcadmin.keytab admin/dc@HZNEW.TONGDUN.COM")
    os.environ['HADOOP_CLASSPATH'] = "/usr/install/libs/mysql-connector-java-5.1.34.jar:/usr/install/tongdunLibraries/td-user-group-mapping-1.0.0.jar:/usr/install/spark-2.4.0-bin-2.6.0-cdh5.15.0-livy/spark-gateway-1.0.0-jar-with-dependencies.jar"
    os.environ['HADOOP_HOME'] = os.environ["CDH_HADOOP_HOME"]
    os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH-5.15.0-1.cdh5.15.0.p0.21/lib64/'
    hadoop_bin = '{0}/bin/hadoop'.format(os.environ['HADOOP_HOME'])
    classpath = subprocess.check_output([hadoop_bin, 'classpath', '--glob'])
    os.environ['CLASSPATH'] = classpath.decode('utf-8')


def writer_dl_table(df, schema, db_table_name, mode="error", rowgroup_size_mb=None):
    # from petastorm.fs_utils import FilesystemResolver
    from pyspark.sql import SparkSession
    from petastorm.etl.dataset_metadata import materialize_dataset
    import pyarrow as pa

    spark = SparkSession.builder.getOrCreate()
    db, table_name = db_table_name.split(".")
    hdfs_path = hive_base_url + db + ".db/" + table_name

    filesystem_factory = lambda: pa.hdfs.connect()
    print(hdfs_path)

    with materialize_dataset(spark, hdfs_path, schema, rowgroup_size_mb, use_summary_metadata=True,
                             filesystem_factory=filesystem_factory):
        df.write.mode(mode).parquet(hdfs_path)


def make_dl_table_reader(db_table_name,schema_fields=None,
                         reader_pool_type='thread', workers_count=10,
                         pyarrow_serialize=False, results_queue_size=50,
                         num_epochs=1):

    from petastorm import make_reader
    db, table_name = db_table_name.split(".")
    hdfs_path = hive_base_url + db + ".db/" + table_name
    return make_reader(hdfs_path,schema_fields=None,
                         reader_pool_type='thread', workers_count=10,
                         pyarrow_serialize=False, results_queue_size=50,
                         num_epochs=1,hdfs_driver="libhdfs")




def generate_petastorm_dataset_test():
    set_env()
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    test_schema = Unischema('test_schema', [
        UnischemaField('id', np.int32, (), ScalarCodec(IntegerType()), False),
        UnischemaField('names',np.string_, (), ScalarCodec(StringType()), False),
    ])

    db_table_name = "ml.tmp_parquet_test"

    rdd = sc.parallelize([(18, "n1"), (19, "n2")])
    df = spark.createDataFrame(rdd, ['id', 'names'])

    writer_dl_table(df, test_schema, db_table_name,mode="overwrite")


def reader_test():
    from petastorm.tf_utils import tf_tensors
    import tensorflow as tf
    db_table_name = "ml.tmp_parquet_test"
    with make_dl_table_reader(db_table_name) as reader:
        row_tensors = tf_tensors(reader)
        with tf.Session() as session:
            for _ in range(2):
                print(session.run(row_tensors))



if __name__ == '__main__':
    generate_petastorm_dataset_test()
