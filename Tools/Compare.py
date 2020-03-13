# encoding = utf-8
# @Author: Hewen
# @Time: 12/31/2019 2:07 PM
# @File: CalSsd.py
import os
import re
import sys
import ssdeep
import winreg
import hashlib
import chardet
import tkinter
import xlwings as xl
from tkinter.messagebox import showwarning
from subprocess import check_call, CalledProcessError
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfilename

path_dir = os.path.dirname(sys.argv[0])


def get_encoding(file_path):
    try:
        with open(file_path, "rb")as file:
            encoding = chardet.detect(file.read())["encoding"]
    except chardet.UniversalDetector:
        return False
    except OSError:
        return False
    else:
        return encoding


def get_install(reg_path, reg_key):
    path_hkey = reg_path.split("\\")[0]
    path_main = reg_path.strip(path_hkey)[1:]
    hkey_dict = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_USERS": winreg.HKEY_USERS
    }
    try:
        try:
            key = winreg.OpenKey(hkey_dict[path_hkey], path_main, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        except FileNotFoundError:
            key = winreg.OpenKey(hkey_dict[path_hkey], path_main, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
    except FileNotFoundError:
        return False
    else:
        result = winreg.QueryValueEx(key, reg_key)[0]
        return result


def save_file(**kwargs):
    _option = {"title": "Save as",
               "filetypes": [("all", ".xlsx",)],
               "initialfile": "imf7_ScanEngine",
               "defaultextension": "xlsx"}
    _option.update(**kwargs)
    excel_path = asksaveasfilename(**_option)
    while excel_path == "":
        showwarning(title="again", message="请重新选择保存的位置和名字")
        excel_path = asksaveasfilename(**_option)
    return excel_path


def choose_file(**kwargs):
    _option = {"title": "Choose Log File",
               "filetypes": [("all", ".log",)],
               "initialfile": "imf7_ScanEngine",
               "defaultextension": "log"}
    _option.update(**kwargs)
    excel_path = askopenfilename(**_option)
    while excel_path == "":
        showwarning(title="again", message="请重新选择文件")
        excel_path = askopenfilename(**_option)
    return excel_path


def choose_folder():
    option = {
        "title": "Choose IMF Log Folder"
    }
    path = askdirectory(**option)
    while path is "":
        path = askdirectory(**option)
    return path


def get_md5(file_path):
    md5 = hashlib.md5()
    try:
        with open(file_path, "rb")as file:
            md5.update(file.read())
            result = md5.hexdigest()
    except OSError:
        return False
    else:
        return result


def get_ssd(file_path):
    try:
        with open(file_path, "rb")as file:
            ssd = ssdeep.hash(file.read())
    except ssdeep.FuzzyLibError:
        return False
    except OSError:
        return False
    else:
        return ssd


def get_compare(ssd1, ssd2):
    try:
        return ssdeep.compare(ssd1, ssd2)
    except ssdeep.FuzzyLibError:
        return False
    except TypeError:
        return False


class UI:
    def __init__(self):
        self.app = tkinter.Tk()
        self.app.geometry("400x400+400+300")
        self.button_7 = self.button(**{"command": self.func_7, "text": "IMF7"})
        self.button_8 = self.button(**{"command": self.func_8, "text": "IMF8"})

        self.button_7.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)
        self.button_8.grid(row=3, column=0, sticky=tkinter.N + tkinter.S)

        self.app.mainloop()

    def button(self, **kwargs):
        option = {}
        option.update(kwargs)
        button = tkinter.Button(self.app, **option)
        return button

    def func_7(self):
        excel = xl.App(visible=False, add_book=False)
        reg_path = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\IObit\IObit Malware Fighter"
        reg_key = "apppath"
        path_folder = get_install(reg_path, reg_key)
        if path_folder:
            path_folder = os.path.join(path_folder, r"log\scan")
        else:
            showwarning(message="请手动选择IMF扫描日志路径")
            path_folder = choose_folder()
        excel_7 = excel.books.add()
        excel_7.sheets.add(name="IMF7多次扫描结果")
        excel_7.sheets["IMF7多次扫描结果"].range("A1").value = ["扫描对象数", "扫描用时", "扫描到的威胁数"]
        num = 1
        for file_name in os.listdir(path_folder):
            file_path = os.path.join(path_folder, file_name)
            with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
                detail = file.read()
                scan_num = re.findall(r"Objects Scanned: (\d*)", detail)
                scan_time = re.findall(r"Time Elapsed: (.*)", detail)
                scan_viru = re.findall(r"Threats Detected: (\d*)", detail)
                result_list = list(zip(scan_num, scan_time, scan_viru))
                num += 1
                excel_7.sheets["IMF7多次扫描结果"].range(f"A{num}").value = result_list
        self.button_7["state"] = "disable"
        save_path = os.path.join(path_dir, "IMF7多次扫描结果.xlsx")
        excel_7.save(save_path)
        excel_7.close()
        showwarning(message="Successful")

    def func_8(self):
        file_path = os.path.join(path_dir, "imf7_ScanEngine.log")
        if os.path.exists(file_path) is False:
            showwarning(title="warning", message="日志不存在, 请重新扫描, 或手动选择日志文件")
            file_path = choose_file()
        self.gen_imf8(file_path)
        self.button_8["state"] = "disable"

    @staticmethod
    def gen_imf8(file_path):
        excel = xl.App(visible=False, add_book=True)
        excel_8 = excel.books.add()
        save_path = os.path.join(path_dir, "IMF8扫描结果.xlsx")
        # 扫描结果
        excel_8.sheets.add(name="IMF8扫描结果")
        excel_8.sheets["IMF8扫描结果"].range("A1").value = ["扫描对象数", "扫描用时", "扫描到的威胁数"]
        with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
            detail = file.read()
        scan_num = re.findall(r"扫描对象数： (\d*)", detail)
        scan_time = re.findall(r"扫描用时：(.*)", detail)
        scan_virus = re.findall(r"扫描到的威胁数： (\d*)", detail)
        excel_8.sheets["IMF8扫描结果"].range("A2").value = list(zip(scan_num, scan_time, scan_virus))

        # 具体SSD
        ssd_path = r"Ssdeep.db"
        target_folder = os.path.join(path_dir, "SSD")
        if os.path.exists(ssd_path):
            if os.path.exists(target_folder) is False:
                os.makedirs(target_folder)
            with open(ssd_path, "r", encoding=get_encoding(ssd_path))as _:
                ssd_dict = {detail.split(",")[0]: detail.split(",")[-1] for detail in _.readlines()}
            with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
                details = file.readlines()
            find_rule = r".*path:(.*?)\|.*scantype:SSDEEP.*dbindex:(\d*)\|"
            ssd_detail = [re.findall(find_rule, line)[0] for line in details if "scantype:SSDEEP" in line]
            ssd_detail = set(ssd_detail)
            excel_8.sheets.add(name="SSD扫描结果")
            excel_8.sheets["SSD扫描结果"].range("A1").value = ["文件地址", "数据库编号", "文件ssd", "数据库ssd", "文件MD5", "ssd比较结果"]
            num = 1
            for scan in ssd_detail:
                num += 1
                file_path = scan[0]
                dbindex = scan[1]
                file_md5 = get_md5(file_path)
                file_ssd = get_ssd(file_path)
                database_ssd = ssd_dict[dbindex]
                compare_result = get_compare(file_ssd, database_ssd)
                scan_detail = [file_path, dbindex, file_md5, file_ssd, database_ssd, compare_result]
                excel_8.sheets["SSD扫描结果"].range(f"A{num}").value = scan_detail
                # 转移文件
                command = f"copy \"{file_path}\" \"{target_folder}\""
                try:
                    check_call(command, shell=True)
                except PermissionError:
                    pass
                except CalledProcessError:
                    pass
        else:
            pass
            # 先不开启
            # ssd_path = choose_file(**{"filetypes": [("all", ".db",)]})
            # if os.path.exists(target_folder)is False:
            #     os.makedirs(target_folder)
            # with open(ssd_path, "r", encoding=get_encoding(ssd_path))as _:
            #     ssd_dict = {detail.split(",")[0]: detail.split(",")[-1] for detail in _.readlines()}
            # with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
            #     details = file.readlines()
            # find_rule = r".*path:(.*?)\|.*scantype:SSDEEP.*dbindex:(\d*)\|"
            # ssd_detail = [re.findall(find_rule, line)[0] for line in details if "scantype:SSDEEP" in line]
            # ssd_detail = set(ssd_detail)
            # excel_8.sheets.add(name="SSD扫描结果")
            # excel_8.sheets["SSD扫描结果"].range("A1").value = ["文件地址", "数据库编号", "文件ssd", "数据库ssd", "文件MD5", "ssd比较结果"]
            # num = 1
            # for scan in ssd_detail:
            #     num += 1
            #     file_path = scan[0]
            #     dbindex = scan[1]
            #     file_md5 = get_md5(file_path)
            #     file_ssd = get_ssd(file_path)
            #     database_ssd = ssd_dict[dbindex]
            #     compare_result = get_compare(file_ssd, database_ssd)
            #     scan_detail = [file_path, dbindex, file_md5, file_ssd, database_ssd, compare_result]
            #     excel_8.sheets["SSD扫描结果"].range(f"A{num}").value = scan_detail
            #     # 转移文件
            #     command = f"copy \"{file_path}\" \"{target_folder}\""
            #     try:
            #         check_call(command, shell=True)
            #     except PermissionError:
            #         pass
            #     except CalledProcessError:
            #         pass
        excel_8.save(save_path)
        excel_8.close()
        showwarning(message="Successful")


if __name__ == "__main__":
    UI()
