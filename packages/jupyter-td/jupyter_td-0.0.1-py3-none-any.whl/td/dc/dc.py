import json,os,requests
from urllib3 import encode_multipart_formdata
from td.contents.util.config import conf

# dc_host = 'http://datacompute.tongdun.me'
# dc_log_url = dc_host + '/v1/jobLog/get/'
# dc_auth_url = dc_host + '/v1/queryAccount?userId='
# dc_exe_url = dc_host + '/v1/jobInstance/add'
# dc_job_state_url = dc_host + '/v1/jobInstance/get/'
#
# dc_resource_upload = dc_host + '/v1/resource/upload'
# dc_resource_del = dc_host + '/v1/resource/del'
# dc_turing_appkey = 'oRVujUonk65ZKfYC'
# dc_turing_appsecret = 'MUQcWhKqmxGwSsjg15nMlQ5GnMeFpjEP'
#
# dc_project_code = 'ml'


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

tlib_url = conf.enki_url

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
        pass
        # display("DC上传资源" + location + file_name + "成功")
        # display("在python代码main()函数前添加# addPkg /user/datacompute/users/{0}/pkg/{1}".format(account,file_name))
    else:
        raise Exception("DC上传资源失败", "失败原因：" + content['message'])


def delete_resource(dc_resource_path, dc_project_code=None):
    account = get_current_account()

    account_info = getAccount(account)
    data = {}
    data['appkey'] = account_info[0]
    data['appsecret'] = account_info[1]
    data['projectCode'] = dc_project_code
    data['location'] = dc_resource_path
    headers = {'Content-Type': 'application/json'}
    # print(data)
    resp = requests.post(dc_resource_del, data=json.dumps(data), headers=headers)
    content = json.loads(resp.text)
    if content['success']:
        pass
        # display("DC资源" + dc_resource_path + "删除成功")
    else:
        raise Exception("DC删除资源失败", "失败原因：" + content['message'])
