import requests
import json
from IPython.display import display
from IPython.display import HTML
import os
from td.contents.util.config import conf
import zipfile
from urllib3 import encode_multipart_formdata

dc_host = conf.getDCHost()
dc_log_url = dc_host + conf.get('dc_log_url')
dc_auth_url = dc_host + conf.get('dc_auth_url')
dc_exe_url = dc_host + conf.get('dc_exe_url')
dc_job_state_url = dc_host + conf.get('dc_job_state_url')
dc_project_code = conf.get('dc_project_code')
dc_resource_upload = dc_host + conf.get('dc_resource_upload')
dc_resource_del = dc_host + conf.get('dc_resource_del')
dc_turing_appkey = conf.get("dc_turing_appkey")
dc_turing_appsecret = conf.get("dc_turing_appsecret")


def get_current_account():
    try:
        return os.environ.get("user_name").replace("@tongdun.cn", "").replace("@tongdun.net", "")
    except:
        raise Exception("查不到用户,请联系管理员!")


def getAccount(account):
    url = dc_auth_url + account + "&appkey=" + dc_turing_appkey + "&appsecret=" + dc_turing_appsecret
    content = requests.get(url).content
    ret = json.loads(content)
    appkey = json.loads(ret['message'])['appkey']
    appsecret = json.loads(ret['message'])['appsecret']
    return [appkey, appsecret]


def jupyter_lab_monitor(jobInstanceCode):
    import time
    current_line_num = 0
    while True:
        content = requests.get(dc_job_state_url + jobInstanceCode).content
        ret = json.loads(content)
        state = ret['data']['status']
        time.sleep(5)
        if state < 5:
            print('state=', state, '等待任务开始运行')
            time.sleep(5)
            continue
        elif state >= 5:  # 运行完毕
            time.sleep(5)  # dc任务的状态和日志并不同步更新，暂停一段时间等待日志更新完毕

        url = dc_log_url + jobInstanceCode
        response = requests.get(url)
        ret = json.loads(response.text)
        lines = ret['message'].splitlines()
        line_num = len(lines)
        if current_line_num < line_num :
            for i in range(current_line_num, line_num):
                print(lines[i])
            current_line_num = line_num

        if state > 5: break


def match_variable(content, params={}):
    import re
    matcher = re.compile("\$\{\w+\}")
    for var in set(matcher.findall(content)):
        var_temp = var[2:-1]
        if params.get(var_temp) is None:
            var_replace = input(var_temp + '参数为空，请输入 ' + var_temp + '=')
        else:
            var_replace = str(params.get(var_temp))
        content = content.replace(var, var_replace)
    return content


def submit(py_file_path, dc_project_code=None, is_overwrite=False, upload_files_list=None, zip_name=None,
           is_need_monitor=True, spark_config={}, **params):
    """

    :param py_file_path: 本地需要上传dc执行包含main(sparkSession)的py文件地址
    :param dc_project_code: 项目代码
    :param is_overwrite: 上传资源是否覆盖同名文件
    :param upload_files_list: 需要被引用其他py文件，只支持同目录下文件
    :param zip_name: 压缩包文件名，被引用文件会保存到该压缩包下
    :param is_need_monitor: 是否监控日志返回
    :param spark_config: 支持输入spark配置，字典类型输入
    :param params:可变长参数，若执行脚本存在${var1}和${var2},可通过submit(..,var1=123,var2=234)输入参数
    :return:
    """
    if dc_project_code is None: dc_project_code = conf.get('dc_project_code')
    try:
        if any([upload_files_list, zip_name]):
            if all([upload_files_list, zip_name]):
                zip_files(upload_files_list, zip_name)
                if is_overwrite:
                    delete_resource(dc_resource_path='/pkg/' + zip_name, dc_project_code=dc_project_code)
                upload_resource(file_name=zip_name, file_path=zip_name, location='/pkg/',
                                dc_project_code=dc_project_code)
            else:
                raise Exception("upload_files_list和zip_name只能全空或者全填！")

        code_content = transform_code(py_file_path, zip_name, params, spark_config)
        submit_code(code_content, dc_project_code, is_need_monitor)
    except Exception as e:
        display(e)
    finally:
        if zip_name is not None and os.path.exists(zip_name):
            os.remove(zip_name)



def submit_func(jar_name, main_class_name, env_conf, job_name="None",input_path="",output_path="",params=[]):
    code_content = ""
    for k, v in env_conf.items():
        code_content = code_content + "set {}={};\n".format(k, v)
    if input_path is not "" and output_path is not "":
        input_path = "\""+input_path+"\""
        output_path = "\""+output_path+"\""

    code_content = code_content + "\n\n{} {} {} {} {}".format(jar_name, main_class_name,input_path,output_path," ".join(params))
    print("脚本代码:\n{}".format(code_content))
    submit_code(code_content, dc_project_code, True, job_type='job', job_name=job_name)


def transform_code(py_file_path, zip_name=None, params={}, spark_config={}):
    if type(spark_config) is not dict:
        raise Exception("spark_config必须为字典类型")

    with open(py_file_path, 'r') as f:
        code_content_lines = f.readlines()

    if zip_name is not None:
        code_content_lines.insert(2, '# addPkg /user/datacompute/users/{0}/pkg/{1}\n'.format(get_current_account(),
                                                                                             zip_name))
    for k, v in spark_config.items():
        code_content_lines.insert(2, '# set {0}={1}\n'.format(k, v))

    code_content = ''.join(code_content_lines)
    code_content = match_variable(code_content, params)
    return code_content


def submit_code(code_content, dc_project_code, is_need_monitor, job_type='python' , job_name = None):
    """

    :param code_content: 代码，string格式
    :param dc_project_code: 项目代码
    :param is_need_monitor: 是否监控日志返回
    :return:
    """
    account = get_current_account()
    try:
        account_info = getAccount(account)
        dict = {}
        dict['appkey'] = account_info[0]
        dict['appsecret'] = account_info[1]
        dict['jobType'] = job_type
        dict['content'] = code_content
        dict['projectCode'] = dc_project_code
        if job_name is not None:
            dict["jobName"] = job_name+'_'+account

        headers = {'Content-Type': 'application/json'}
        resp = requests.post(dc_exe_url, data=json.dumps(dict), headers=headers)
        ret = json.loads(resp.text)
        jobInstanceCode = ret['message']
        href_url = dc_host + '/jobMgr/instMonitor?instanceCode=' + jobInstanceCode
        if href_url.find('datacompute.tongdun.me') != -1:
            if href_url.find('http') != -1:
                href_url = href_url.replace('http', 'https')
            else:
                href_url = 'https://' + href_url
        display(HTML("<a href={0}>dc作业监控</a>".format(href_url)))
        if is_need_monitor:
            jupyter_lab_monitor(jobInstanceCode)
    except Exception as e:
        display('dc任务提交失败！')
        raise Exception(e)


def upload_resource(file_name, file_path, location, dc_project_code):
    """

    :param file_name: 保存文件名
    :param file_path: 本地文件地址
    :param location: dc资源地址
    :param dc_project_code: 项目编码
    :return:
    """
    account = get_current_account()
    account_info = getAccount(account)
    data = {}
    data['appkey'] = account_info[0]
    data['appsecret'] = account_info[1]
    data['location'] = location
    data['file'] = (file_name, open(file_path, 'rb').read())
    data['projectCode'] = dc_project_code
    encode_data = encode_multipart_formdata(data)
    data = encode_data[0]
    headers = {'Content-Type': encode_data[1]}
    resp = requests.post(dc_resource_upload, data=data, headers=headers)
    content = json.loads(resp.text)
    if content['success']:
        display("DC上传资源" + location + file_name + "成功")
        # display("在python代码main()函数前添加# addPkg /user/datacompute/users/{0}/pkg/{1}".format(account,file_name))
    else:
        raise Exception("DC上传资源失败", "失败原因：" + content['message'])


def delete_resource(dc_resource_path, dc_project_code=None):
    account = get_current_account()
    if dc_project_code is None: dc_project_code = conf.get('dc_project_code')

    account_info = getAccount(account)
    data = {}
    data['appkey'] = account_info[0]
    data['appsecret'] = account_info[1]
    data['projectCode'] = dc_project_code
    data['location'] = dc_resource_path
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(dc_resource_del, data=json.dumps(data), headers=headers)
    content = json.loads(resp.text)
    if content['success']:
        display("DC资源" + dc_resource_path + "删除成功")
    else:
        raise Exception("DC删除资源失败", "失败原因：" + content['message'])


def zip_files(files, zip_name):
    with zipfile.ZipFile(zip_name, "w") as myzip:
        for file in files:
            display('compressing', file)
            myzip.write(file)
    display('compressing finished')


if __name__ == '__main__':
    print(dc_auth_url)
