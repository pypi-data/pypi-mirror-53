import requests
def save_lab_project(filename):
    global turing_urls,global_lab_path
    data = {"path" : global_lab_path}
    files = {
       "file" : open(filename, "rb")
    }
    turing_urls_list = turing_urls.split(",")
    attempt_num = 1
    status = False
    while not status and attempt_num < 3:
        for turing_url in turing_urls_list:
            try:
                r = requests.post(turing_url + "/jupyterlab/upload", data, files=files)
                if r.status_code == 200:
                    print("保存成功")
                    status = True
                    break
            except:
                pass
        attempt_num += 1
    if not status:
        print("保存失败,请重试!")

turing_urls = "http://127.0.0.1:8080"
global_lab_path = "/notebooks/f4/"

save_lab_project("/Users/wqs/a.py")