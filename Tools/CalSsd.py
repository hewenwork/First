# encoding = utf-8
# @Author: Hewen
# @Time: 12/31/2019 2:07 PM
# @File: CalSsd.py
import ctypes
import os
import re
import sys
import winreg
import ssdeep
import hashlib
import chardet
import tkinter
import logging
import xlwings as xl
from threading import Thread
from tkinter.messagebox import showwarning
from tkinter.filedialog import asksaveasfilename, askdirectory


logging.basicConfig(**{
    "filemode": "a+",
    "filename": f"{os.path.basename(__file__)}_debug.log",
    "level": logging.INFO,
    "format": "%(asctime)s--: %(lineno)d: %(funcName)s: %(levelname)s - %(message)s"
})
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
md5 = hashlib.md5()
path_dir = os.path.dirname(sys.argv[0])

excel = xl.App(visible=False, add_book=False)
new_excel = excel.books.add()


def get_encoding(file_path):
    try:
        with open(file_path, "rb")as file:
            encoding = chardet.detect(file.read())["encoding"]
    except Exception as e:
        log.info(e)
        return False
    else:
        return encoding


def get_install():
    reg_path_64 = r"SOFTWARE\WOW6432Node\IObit\IObit Malware Fighter"
    try:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path_64, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        except FileNotFoundError:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path_64, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
    except FileNotFoundError:
        return False
    else:
        return winreg.QueryValueEx(key, "apppath")[0]


def choose_file():
    _option = {"title": "Save as",
               "filetypes": [("all", ".xlsx",)],
               "initialfile": "Your Name",
               "defaultextension": "xlsx"}
    excel_path = asksaveasfilename(**_option)
    while excel_path == "":
        showwarning(title="again", message="请重新选择保存的位置和名字")
        excel_path = asksaveasfilename(**_option)
    return excel_path


def choose_folder():
    folder_path = askdirectory()
    while folder_path == "":
        folder_path = askdirectory()
    return folder_path


class CalSsd:

    def __init__(self):
        path_database = os.path.join(path_dir, r"SsDeep.db")
        path_scan = os.path.join(path_dir, r"imf7_ScanEngine.log")
        with open(path_database, encoding="utf-8")as file:
            self.ssd_dict = {detail.split(",")[0]: detail.split(",")[-1] for detail in file.readlines()}
        # 写入excel
        new_excel.sheets.add(name="Ssd测试结果")
        rows = 1
        new_excel.sheets["Ssd测试结果"].range(f"A{rows}").value = ["文件地址", "数据库编号", "文件MD5", "文件ssd", "数据库ssd", "ssd比较结果"]
        for scan in self.get_scan(path_scan):
            rows += 1
            file_path = scan[0]
            dbindex = scan[1]
            file_md5 = self.get_md5(file_path)
            file_ssd = self.get_ssd(file_path)
            database_ssd = self.ssd_dict[dbindex]
            compare_result = self.get_compare(file_ssd, database_ssd)
            scan_detail = [file_path, dbindex, file_md5, file_ssd, database_ssd, compare_result]
            new_excel.sheets["Ssd测试结果"].range(f"A{rows}").value = scan_detail

        save_path = os.path.join(path_dir, "Ssd测试结果.xlsx")
        new_excel.save(choose_file())
        new_excel.close()
        showwarning(message="Successful")

    @staticmethod
    def get_ssd(file_path):
        try:
            with open(file_path, "rb")as file:
                ssd = ssdeep.hash(file.read())
        except Exception as e:
            log.info(f"{file_path}--{e}")
            return False
        else:
            return ssd

    @staticmethod
    def get_compare(ssd1, ssd2):
        try:
            return ssdeep.compare(ssd1, ssd2)
        except Exception as e:
            log.info(f"compare error , {e}")
            return False

    @staticmethod
    def get_md5(file_path):
        try:
            with open(file_path, "rb")as file:
                md5.update(file.read())
                result = md5.hexdigest()
        except Exception as e:
            log.info(e)
            return False
        else:
            return result

    @staticmethod
    def get_scan_dict():
        # path_database = os.path.join(path_dir, "SsDeep.db")
        # path_scan = os.path.join(path_dir, "imf7_ScanEngine.log")
        path_scan = r"C:\Users\hewen\Desktop\sacn_result\win732.log"

        with open(path_scan, "r", encoding=get_encoding(path_scan))as file:
            detail = file.readlines()
        try:
            scan_list = []
            for line in detail:
                scan_dict = {}
                if "scantype:SSDEEP" in line:
                    scan_path = re.findall(r".*path:(.*?)\|.*scantype:SSDEEP.*", line)
                    scan_index = re.findall(r"dbindex:(\d*)\|", line)
                    scan_dict["file_path"] = scan_path[0]
                    scan_dict["dbindex"] = scan_index[0]
                    scan_list.append(scan_dict)
        except Exception as e:
            log.info(e)
            return False
        else:
            return scan_list
        finally:
            file.close()

    @staticmethod
    def creat_excel(scan_list):
        new_excel.sheets.add(name="Ssd测试结果")
        rows = 1
        new_excel.sheets["Ssd测试结果"].range(f"A{rows}").value = ["文件地址", "数据库编号", "文件ssd", "数据库ssd", "文件MD5", "ssd比较结果"]
        for scan__dict in scan_list:
            rows += 1
            info_list = list(scan__dict.values())
            new_excel.sheets["Ssd测试结果"].range(f"A{rows}").value = info_list

    @staticmethod
    def get_scan(path_scan):
        find_rule = r".*path:(.*?)\|.*scantype:SSDEEP.*dbindex:(\d*)\|"
        with open(path_scan, "r", encoding=get_encoding(path_scan))as file:
            detail = file.readlines()
        details = [re.findall(find_rule, line)[0] for line in detail if "scantype:SSDEEP" in line]
        return details


class GetLog:

    def __init__(self, file_path):
        result = self.get_log_detial(file_path)
        if result:
            self.write_excel(result)

    @staticmethod
    def write_excel(result):
        new_excel.sheets.add(name="多次扫描结果")
        new_excel.sheets["多次扫描结果"].range("A1").value = ["扫描对象数", "扫描用时", "扫描到的威胁数"]
        for line in result:
            num = result.index(line) + 2
            new_excel.sheets["多次扫描结果"].range(f"A{num}").value = line

    @staticmethod
    def get_log_detial(file_path):
        try:
            with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
                detail = file.read()
                scan_num = re.findall(r"扫描对象数： (\d*)", detail)
                scan_time = re.findall(r"扫描用时：(.*)", detail)
                scan_viru = re.findall(r"扫描到的威胁数： (\d*)", detail)
                result_list = list(zip(scan_num, scan_time, scan_viru))
        except Exception as e:
            log.info(e)
            return False
        else:
            return result_list


class UI:
    def __init__(self):
        self.app = tkinter.Tk()
        self.app.geometry("200x200+400+300")
        _7 = {
            "text": "IMF7",
            "command": self.func_7
        }
        self.button_7 = tkinter.Button(self.app, **_7)
        _8 = {
            "text": "IMF8",
            "command": self.func_8
        }
        self.button_8 = tkinter.Button(self.app, **_8)

        self.button_7.grid(row=0, column=0, sticky=tkinter.N + tkinter.S)
        self.button_8.grid(row=3, column=0, sticky=tkinter.N + tkinter.S)
        self.label = tkinter.Label(self.app, text="准备就绪")

        self.label.grid(row=4, column=0, sticky=tkinter.N + tkinter.S)
        self.app.mainloop()

    def func_7(self):
        if get_install():
            folder_path = os.path.join(get_install(), r"log\scan")
        else:
            showwarning(message="请手动选择IMF扫描日志路径")
            folder_path = askdirectory()
        new_excel.sheets.add(name="多次扫描结果")
        new_excel.sheets["多次扫描结果"].range("A1").value = ["扫描对象数", "扫描用时", "扫描到的威胁数"]
        num = 1
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, encoding=get_encoding(file_path), mode="r")as file:
                detail = file.read()
                scan_num = re.findall(r"Objects Scanned: (\d*)", detail)
                scan_time = re.findall(r"Time Elapsed: (.*)", detail)
                scan_viru = re.findall(r"Threats Detected: (\d*)", detail)
                result_list = list(zip(scan_num, scan_time, scan_viru))
                num += 1
                new_excel.sheets["多次扫描结果"].range(f"A{num}").value = result_list
        self.button_7["state"] = "disable"
        save_path = os.path.join(path_dir, "多次扫描结果.xlsx")
        new_excel.save(save_path)
        new_excel.close()
        showwarning(message="Successful")

    def func_8(self):
        self.label["text"] = "正在读取数据库, 请耐心等待"
        thread = Thread(target=CalSsd)
        thread.setDaemon(True)
        thread.start()
        self.label["text"] = "处理完毕"
        self.button_8["state"] = "disable"


if __name__ == "__main__":
    UI()
