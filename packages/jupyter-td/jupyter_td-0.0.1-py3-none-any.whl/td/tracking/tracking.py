from __future__ import print_function

import json
import os
import time
import traceback

import requests

env = os.environ

run_uuid = env.get("tracking_run_uuid", "")
butler_ip = env.get("tracking_butler_ip", "")
dfs_ip = env.get("tracking_dfs_ip", "")
namespace = env.get("tracking_namespace", "")
ttl = env.get("tracking_dfs_ttl", "")


# run_uuid = "adfadsf"
# butler_ip = "127.0.0.1:8089"
# dfs_ip = "http://10.57.17.156:8080/rest/api"
# namespace = "test1"


def log_param(key, value):
    timestamp = time.time()
    try:
        params = {"run_uuid": run_uuid, "key": key, "value": value, "timestamp": timestamp}
        res = requests.get("http://" + butler_ip + "/tracking/logParam?", params=params)
        return json.loads(res.content)["status"]
    except Exception as e:
        print(e.args)
        print(u'traceback.format_exc():\n%s' % traceback.format_exc())


def log_metric(key, value, step):
    timestamp = time.time()
    try:
        params = {"run_uuid": run_uuid, "key": key, "value": value, "step": step, "timestamp": timestamp}
        res = requests.get("http://" + butler_ip + "/tracking/logMetric?", params=params)
        return json.loads(res.content)["status"]
    except Exception as e:
        print(e.args)
        print(u'traceback.format_exc():\n%s' % traceback.format_exc())


def log_tag(key, value):
    timestamp = time.time()
    try:
        params = {"run_uuid": run_uuid, "key": key, "value": value, "timestamp": timestamp}
        res = requests.get("http://" + butler_ip + "/tracking/logTag?", params=params)
        return json.loads(res.content)["status"]
    except Exception as e:
        print(e.args)
        print(u'traceback.format_exc():\n%s' % traceback.format_exc())


def log_artifact(file_path, folder=""):
    try:
        path = os.path.abspath(file_path)
        name = os.path.basename(path)
        if folder == "":
            folder = "./"
        if os.path.isdir(path):
            i = 1
            for root, dirs, files in os.walk(path):
                if i > 1:
                    break
                for dir in dirs:
                    if folder == "./":
                        nextFolder = folder + dir
                    else:
                        nextFolder = folder + "/" + dir
                    log_artifact(os.path.join(root, dir), nextFolder)
                    print(os.path.join(root, dir))
                    print(nextFolder)
                for file in files:
                    log_artifact(os.path.join(root, file), folder)
                i = i + 1

        elif os.path.isfile(path):
            # ttl = 60*60*24*365
            ttl = 60 * 60 * 24
            command = 'curl -vvv -F "namespace=' + namespace + '" -F "length="' + str(
                os.path.getsize(path)) + ' -F "name=' + name + '" -F "ttl=' + str(
                ttl) + '"   -F "filedata=@' + file_path + '" ' + dfs_ip
            result = os.popen(command)
            print("popen result: " + result.read())
            resp = json.loads(result.read())
            fileId = resp["data"]

            params = {"run_uuid": run_uuid, "fileId": fileId, "path": folder, "name": name}
            res = requests.get("http://" + butler_ip + "/tracking/logArtifact?", params=params)
            print(res.content)
            return json.loads(res.content)["status"]
    except Exception as e:
        print(e.args)
        print(u'traceback.format_exc():\n%s' % traceback.format_exc())
