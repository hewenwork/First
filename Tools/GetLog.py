# encoding = utf-8
# @Author: Hewen
# @Time: 1/22/2020 3:29 PM
# @File: GetLog.py
import os
import re
import sys
import winreg
import zipfile
import hashlib
from threading import Thread

import ssdeep
import logging
import chardet
import xlwings as xl
from tkinter import Tk, Button, Label
from tkinter.messagebox import showinfo, askyesno
from tkinter.filedialog import askopenfilename, askdirectory

program_dir = os.path.dirname(sys.argv[0])
log = logging.getLogger(__name__)
logging.basicConfig(
    **{
        "level": logging.INFO,
        "format": "%(asctime)s - %(lineno)s - %(message)s",
        "filename": f"{program_dir}\\{__name__}_debug.log"
    })
log.addHandler(logging.StreamHandler())
ssdeep_path = os.path.join(os.path.dirname(sys.argv[0]), "Ssdeep.db")
file_dir = os.path.dirname(sys.argv[0])


def generate_excel(file_path, **kwargs):
    excel = xl.App(visible=False, add_book=False)
    new_excel = excel.books.add()
    for sheet, data in kwargs.items():
        new_excel.sheets.add(name=sheet)
        for row, value in data.items():
            new_excel.sheets[sheet].range(f"A{row}").value = value
    new_excel.save(file_path)
    new_excel.close()


def encoding(file_path):
    try:
        with open(file_path, "rb")as file:
            return chardet.detect(file.read())["encoding"]
    except Exception as e:
        showinfo(title="warning", message=f"读取文件失败\n{file_path}\n{e}")
        return "utf-8"


class GetLog:

    @staticmethod
    def get_imf8_log_path():
        file_name = r"imf7_ScanEngine.log"
        file_path = os.path.join(program_dir, file_name)
        if os.path.exists(file_path):
            return file_path
        else:
            Tk().withdraw()
            title = "选择日志文件"
            message = "当前位置下没有imf7_ScanEngine.log文件, 请确认\n点击Yes手动选择文件\n点击No退出选择"
            if askyesno(title, message):
                return askopenfilename()
            else:
                return False

    @staticmethod
    def get_imf7_log_dir():
        defaut_dir_64 = r"C:\Program Files (x86)\IObit\IObit Malware Fighter\log\scan"
        defaut_dir_32 = r"C:\Program Files\IObit\IObit Malware Fighter\log\scan"
        if os.path.exists(defaut_dir_64):
            return defaut_dir_64
        elif os.path.exists(defaut_dir_32):
            return defaut_dir_32
        try:
            reg_path_64 = r"SOFTWARE\WOW6432Node\IObit\IObit Malware Fighter"
            reg_32 = (winreg.HKEY_LOCAL_MACHINE, reg_path_64, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
            reg_64 = (winreg.HKEY_LOCAL_MACHINE, reg_path_64, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            try:
                key = winreg.OpenKey(*reg_32)
            except FileNotFoundError:
                key = winreg.OpenKey(*reg_64)
            result = winreg.QueryValueEx(key, "apppath")[0]
            return result
        except FileNotFoundError:
            Tk().withdraw()
            if askyesno("?????", "没有找到IMF安装目录,\n点击Yes手动选择log文件夹,\n点击No退出"):
                return askdirectory()
            else:
                return False

    @staticmethod
    def get_imf7_log_list(file_path):
        try:
            with open(file_path, "r", encoding=encoding(file_path))as file:
                content = file.read()
                scan_num = re.findall(r"Objects Scanned: (\d*)", content)[0]
                scan_time = re.findall(r"Time Elapsed: (.*)", content)[0]
                scan_viru = re.findall(r"Threats Detected: (\d*)", content)[0]
                return [scan_num, scan_time, scan_viru]
        except Exception as e:
            return e

    def generate_imf7(self):
        dir_path = self.get_imf7_log_dir()
        if dir_path is False:
            return
        log_dict = {
            "IMF7扫描结果": {1: ["扫描对象数", "扫描用时", "扫描到的威胁数"]},
        }
        file_path_list = [os.path.join(dir_path, file_name) for file_name in os.listdir(dir_path)]
        for file_path in file_path_list:
            row = file_path_list.index(file_path) + 2
            result = self.get_imf7_log_list(file_path)
            if type(result) is not list:
                return f"{file_path}, {result}"
            else:
                result_dict = {row: result}
                log_dict["IMF7扫描结果"].update(result_dict)
        save_path = os.path.join(file_dir, "IMF7扫描结果.xlsx")
        generate_excel(save_path, **log_dict)

    def generate_imf8(self):
        file_path = self.get_imf8_log_path()
        if file_path is False:
            return False
        log_dict = {
            "IMF8扫描结果": {1: ["扫描对象数", "扫描用时", "扫描到的威胁数"]},
            "IMF8SSD扫描结果": {1: ["文件地址", "数据库编号", "文件ssd", "数据库ssd", "文件MD5", "ssd比较结果"]}
        }
        with open(file_path, "r", encoding=encoding(file_path))as file:
            content = file.read()
        scan_num = re.findall(r"扫描对象数：(.*)", content)
        scan_time = re.findall(r"扫描用时：(.*)", content)
        scan_viru = re.findall(r"扫描到的威胁数：(.*)", content)
        result = list(zip(scan_num, scan_time, scan_viru))
        save_path = os.path.join(file_dir, "IMF8扫描结果.xlsx")
        for detail in result:
            detail_dict = {result.index(detail) + 2: list(detail)}
            log_dict["IMF8扫描结果"].update(detail_dict)
        if os.path.exists(ssdeep_path) is False:
            generate_excel(save_path, **log_dict)
            return True
        with open(file_path, "r", encoding=encoding(file_path))as file:
            content_lines = file.readlines()
        ssd_dict = self.get_ssd_dict()
        find_rule = r".*path:(.*?)\|.*scantype:SSDEEP.*dbindex:(\d*)\|"
        ssd_detials = list(set([re.findall(find_rule, line)[0] for line in content_lines if "scantype:SSDEEP" in line]))
        compress_file = os.path.join(file_dir, "ssdeepfile.zip")
        for line in ssd_detials:
            ssd_file_path = line[0]
            ssd_index = line[-1]
            real_ssd = self.get_ssd(ssd_file_path)
            database_ssd = ssd_dict[ssd_index]
            real_md5 = self.get_md5(ssd_file_path)
            ssd_compare = self.get_compare(real_ssd, database_ssd)
            row = ssd_detials.index(line) + 2
            info_list = [ssd_file_path, ssd_index, real_ssd, database_ssd, real_md5, ssd_compare]
            log_dict["IMF8SSD扫描结果"].update({row: info_list})
        all_file_list = [real_file[0] for real_file in log_dict["IMF8SSD扫描结果"].values()]
        self.get_all_file(compress_file, all_file_list[1:])
        generate_excel(save_path, **log_dict)
        return True

    @staticmethod
    def get_ssd(file_path):
        try:
            with open(file_path, "rb")as file:
                return ssdeep.hash(file.read())
        except Exception as e:
            return str(e)

    @staticmethod
    def get_compare(ssd1, ssd2):
        try:
            return ssdeep.compare(ssd1, ssd2)
        except Exception as e:
            return str(e)

    @staticmethod
    def get_md5(file_path):
        try:
            with open(file_path, "rb")as file:
                return hashlib.md5.update(file.read()).hexdigest()
        except Exception as e:
            return str(e)

    @staticmethod
    def get_ssd_dict():
        try:
            with open(ssdeep_path, "r", encoding=encoding(ssdeep_path))as file:
                result = {line.split(",")[0]: line.split(",")[-1] for line in file.readlines()}
                return result
        except Exception as e:
            return str(e)

    @staticmethod
    def get_all_file(compress_path, file_list):
        com = zipfile.ZipFile(compress_path, mode="a", compression=zipfile.ZIP_STORED, allowZip64=False)
        for file_path in file_list:
            if os.path.exists(file_path):
                try:
                    com.write(file_path)
                except Exception as e:
                    log.info(f"{file_path}, {e}")


class Ui:
    def __init__(self):
        self.app = Tk()
        self.app.geometry("400x400+400+300")
        _7 = {
            "text": "IMF7",
            "command": self.func_7
        }
        self.button_7 = Button(self.app, **_7)
        _8 = {
            "text": "IMF8",
            "command": self.func_8
        }
        self.button_8 = Button(self.app, **_8)

        self.button_7.grid(row=0, column=0)
        self.button_8.grid(row=3, column=0)
        self.label = Label(self.app, text="准备就绪")

        self.label.grid(row=4, column=0)
        self.app.mainloop()

    @staticmethod
    def func_7():
        try:
            GetLog().generate_imf7()
            showinfo(message="Successful")
        except Exception as e:
            showinfo(e)

    def func_8(self):
        self.label["text"] = "正在读取数据库, 请耐心等待"
        thread = Thread(target=GetLog().generate_imf8)
        # thread.setDaemon(True)
        thread.start()
        self.label["text"] = "开始处理"

        while thread.isAlive():
            print(thread.isAlive())
            if Thread.is_alive(thread):
                self.label["text"] = "处理完毕"
                self.button_8["state"] = "disable"
                break


if __name__ == "__main__":
    Ui()
