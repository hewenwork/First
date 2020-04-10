import os
import re
import json
from datetime import datetime
from requests_html import HTMLSession

date_today = datetime.today().strftime("%Y-%m-%d")
save_dir = r"C:\Users\hewen\Desktop\yuwenjian\wc\ywj\%s" % date_today  # r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集\源文件"
if os.path.exists(save_dir) is False:
    os.makedirs(save_dir)
combine_dir = r"C:\Users\hewen\Desktop\yuwenjian"  # r"\\192.168.1.254\部门共享\TEST\朱亚玲\IMF\IMF手动分析\自动收集"
combine_path = os.path.join(combine_dir, f"{date_today}SigN.db")


def login():
    session = HTMLSession()
    data = {
        "username": "hewen",
        "password": "hewen"
    }
    url = "http://192.168.1.19/imfsmart/interface/serverlogin.php"
    if session.post(url, data=data).status_code == 200:
        print("login successful")
        return session
    else:
        exit("login Failed")


def run(start, end):
    session = login()
    data = {
        "pagemaxitems": 15,
        "cpage": -1,
        "action": "gettasks"
    }
    link = "http://192.168.1.19/imfsmart/interface/it_taskmanager.php"
    stop = True
    while stop:
        data["cpage"] += 1
        response = session.post(link, data=data).text
        result = json.loads(response[3:])
        stop = False
        for values in result["tasks"]:
            taskid = values["taskid"]
            completetime = values["completetime"]
            if completetime is "":
                print("file has be analysis, continue.")
                continue
            else:
                file_date = datetime.strptime(completetime, "%Y-%m-%d %H:%M:%S").date()
                if file_date > end:
                    print(f"there has`t data of {file_date}")
                if start <= file_date <= end:
                    print(f"download data, datetime: {file_date}, taskid: {taskid}.")
                    file_path = os.path.join(save_dir, f"{taskid}.db")
                    file_link = f"http://192.168.1.19:8000/{taskid}.db?action=downdb&taskid={taskid}"
                    with open(file_path, "wb")as file:
                        file.write(session.get(file_link).content)
                elif file_date < start:
                    print(f"stop requests, {file_date} has`t match rule.")
                    stop = False
                    break
    with open(combine_path, "wb")as file:
        for file_name in os.listdir(save_dir):
            file_path = os.path.join(save_dir, file_name)
            with open(file_path, "rb")as _file:
                file.write(_file.read())


def input_check(what):
    result = input(u"请输入%s下载的日期, 格式XXXX-XX-XX, 如2019-09-01\n" % what)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", result):
        return result
    else:
        print(u"\r输入错误, 请重新输入. 格式XXXX-XX-XX, 如2019-09-01\n")
        input_check(what)


if __name__ == "__main__":
    a = datetime.strptime(input_check("开始"), "%Y-%m-%d").date()
    b = datetime.strptime(input_check("结束"), "%Y-%m-%d").date()
    print(a, b)
    run(a, b)
