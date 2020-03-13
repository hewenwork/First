import os
import re
import ssdeep
import chardet
import hashlib
import xlwings as xl
from tkinter import Tk
from datetime import datetime
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename, askdirectory

database_path = r"SsDeep.db"
ssdeep_re = r"^.*?, SSDEEP, .*?,.*?,.*?$"
database_dict = {
    line.split(",")[0].replace(" ", ""): line.split(",")[-1].strip("\n")
    for line in open(database_path, "r", encoding="utf-8").readlines()
}
excel = xl.App(visible=False, add_book=False)
new_excel = excel.books.add()


def get_file_md5(file_path):
    with open(file_path, "rb")as file:
        return hashlib.md5(file.read()).hexdigest()


def encoding(file_path):
    with open(file_path, "rb")as file:
        return chardet.detect(file.read())["encoding"]


def get_compare(ssd_true, ssd_database):
    if ssd_database == "file not exists":
        return "file not exists"
    try:
        num = ssdeep.compare(ssd_true, ssd_database)
        return num
    except Exception as e:
        return False


def get_ssdeep(file_path):
    if os.path.exists(file_path) is False:
        return "file not exists"
    try:
        with open(file_path, "rb")as file:
            return ssdeep.hash(file.read())
    except Exception as e:
        return False


def get_log():
    time_now = datetime.strftime(datetime.today(), "%Y%m%d%H%M%S")
    new_excel.sheets.add(name=f"{time_now}")
    rows = 1
    new_excel.sheets[f"{time_now}"].range(f"A{rows}").value = ["文件名", "数据库编号", "数据库ssd", "文件ssd", "ssd比较结果"]
    log_path = get_log_path()
    dir_path = get_diction_dir()
    with open(log_path, "r", encoding="utf-16")as file:
        for line in file.readlines():
            if re.match(ssdeep_re, line) is not None:
                ssdeep_path = re.findall(r"^.*?, SSDEEP, (.*?),.*?,.*?$", line)[0]
                ssdeep_num = re.findall(r"^.*?, SSDEEP, .*?, (.*?),.*?$", line)[0]
                file_name = os.path.basename(ssdeep_path)
                file_path = os.path.join(dir_path, file_name)
                ssdeep_detail = database_dict[ssdeep_num]
                real_ssdeep = get_ssdeep(file_path)
                compare = get_compare(database_dict[ssdeep_num], get_ssdeep(file_path))
                rows += 1
                result_list = [file_name, ssdeep_num, ssdeep_detail, real_ssdeep, compare]
                new_excel.sheets[f"{time_now}"].range(f"A{rows}").value = result_list
    return askokcancel(message="complete, click OK to Next one, \nclick Cancel to exit")


def get_log_path():
    Tk().withdraw()
    log_path = askopenfilename()
    while os.path.exists(log_path) is False:
        log_path = askopenfilename()
    return log_path


def get_diction_dir():
    Tk().withdraw()
    file_diction = askdirectory()
    while os.path.isdir(file_diction) is False:
        file_diction = askdirectory()
    return file_diction


while True:
    if get_log() is False:
        save_path = os.path.join(os.path.dirname(__file__), f"对比结果.xlsx")
        new_excel.save(save_path)
        new_excel.close()
        break
