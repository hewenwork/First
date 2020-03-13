# encoding = utf-8
# @Author: Hewen
# @Time: 10/16/2019 12:19 PM
# @File: MakeRar.py
import re
import os
import sys
import shutil
import tkinter
import hashlib
import datetime
import tkinter.dialog
import tkinter.messagebox
from tkinter import filedialog
from configparser import ConfigParser, NoSectionError
from subprocess import check_output, SubprocessError


def show_exit(message):
    tkinter.Tk().withdraw()
    tkinter.messagebox.showwarning(message=message)
    exit()


def _start():
    tkinter.Tk().withdraw()
    manual_info = u'''
程序为SmartCCL交换样本制作:
- 自动跳过周六周天. 
- 交换样本默认大小在500M以下, 需自定义大小请在设置文件setting.ini中修改split_size
- 样本制作源默认为G:\\urlhash目录下样本. 已使用的会默认添加前缀[已交换]
- 目前仅支持zip格式. 需要修改来源文件夹请修改设置文件source_dir节点
- 若要手动选择文件或文件夹, 请修改设置文件节点Mode=Manual, 然后再运行此程序. 注意: 文件可alt + 鼠标左键多选
- 若要自动运行请请修改设置文件节点Mode=Auto, 然后再运行此程序
- ...
    '''
    setting_info = '''
[main]
source_dir=G:\\urlhaus
upload_dir=G:\\Exchange\\Upload
Mode=Auto
split_size=524288000
'''
    if os.path.exists(r"Manual.txt") is False:
        with open(r"Manual.txt", "w", encoding="utf-8")as Manual:
            Manual.write(manual_info)
    if os.path.exists(r"Setting.ini") is False:
        with open(r"Setting.ini", "w", encoding="utf-8")as Setting:
            Setting.write(setting_info)


def write_Error(error):
    with open(r"Error.log", "a+")as file:
        line = f"{datetime.datetime.now()}: {error}\n"
        file.write(line)


def excu_command(command):
    try:
        check_output(command, shell=True)
    except SubprocessError:
        write_Error(SubprocessError)
        return False
    else:
        return True


try:
    _start()
    con = ConfigParser()
    con.read(r"Setting.ini")
    upload_dir = con.get("main", "upload_dir")
    split_size = int(con.get("main", "split_size"))
    mode = con.get("main", "Mode")
except NoSectionError:
    info = f"设置文件错误:{NoSectionError}\n重新配置设置文件, 然后重启程序"
    show_exit(message=info)


class MakeRar:

    def __init__(self):
        if mode == "Auto":
            source_dir = con.get("main", "source_dir")
            file_list = []
            total_size = 0
            for file_path in self.file_path_list(source_dir):
                if "[已上传]" not in file_path and total_size <= split_size and file_path[-4:] == ".zip":
                    total_size += os.path.getsize(file_path)
                    file_list.append(file_path)
            self.deal_file(file_list)
        elif mode == "Manual":
            result = self.choose()
            if result == u"选择文件夹":
                folder = filedialog.askdirectory(initialdir=r"G:")
                self.deal_fodler(folder)
            else:
                all_path = self.choose_files()
                self.deal_file(all_path)
        else:
            message = u"参数错误, 请在设置文件中设置Mode方式(Auto, Manual), 然后重启程序"
            show_exit(message=message)

    @staticmethod
    def choose():
        result_dict = {
            0: u"选择文件夹",
            1: u"选择文件"
        }
        option = {
            "title": u"选择",
            "text": u"选择要执行的文件或文件夹. 文件可以按Ctrl + 鼠标左键多次选择! ",
            "bitmap": "questhead",
            "default": 0,
            "strings": (result_dict[0], result_dict[1])
        }
        result = tkinter.dialog.Dialog(None, **option).num
        return result_dict[result]

    @staticmethod
    def choose_files():
        total_size = 0
        all_path = ()
        path_tuple = filedialog.askopenfilenames(initialdir=r"G:")
        try:
            all_path += path_tuple
        except TypeError:
            message = u"错误操作, 请重试"
            show_exit(message)
        for file_path in all_path:
            total_size += os.path.getsize(file_path)
        while total_size <= 1024 * 1024 * 1024:
            message = u"点击OK添加更多的文件, 可以同时选择多个文件哦!"
            tkinter.messagebox.showwarning(title=u"文件过小", message=message)
            path_tuple = filedialog.askopenfilenames(initialdir=r"G:")
            for file_path in all_path:
                total_size += os.path.getsize(file_path)
            try:
                all_path += path_tuple
            except TypeError:
                message = u"错误操作, 请重试"
                show_exit(message)
        return all_path

    @staticmethod
    def get_last_upload_date():
        file_list = []
        for file_name in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, file_name)
            if re.match(r"^.*samples-\d{8}\.rar$", file_path) and os.path.isfile(file_path):
                file_list.append(file_path)
        file_list.sort()
        format_data = os.path.split(file_list[-1])[-1][8:-4]
        last_upload_data = datetime.datetime.strptime(format_data, "%Y%m%d")
        return last_upload_data

    @staticmethod
    def file_path_list(folder):
        path_list = []
        try:
            file_list = os.listdir(folder)
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)
            message = u"没有选择任何文件, 请重新运行程序进行选择"
            show_exit(message=message)
        else:
            for file_name in file_list:
                file_path = os.path.join(folder, file_name)
                try:
                    if os.path.exists(file_path):
                        path_list.append(file_path)
                except Exception as e:
                    write_Error(e)
        return path_list

    @staticmethod
    def file_md5(file_path):
        md5_object = hashlib.md5()
        try:
            with open(file_path, "rb")as file:
                md5_object.update(file.read())
            md5_result = md5_object.hexdigest()
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)
            return False
        else:
            return md5_result

    @staticmethod
    def rename_by(file_path, new_name):
        if os.path.exists(file_path):
            file_md5 = MakeRar.file_md5(file_path)
            file_dir = os.path.dirname(file_path)
            new_path = os.path.join(file_dir, new_name)
            if os.path.exists(new_path):
                if file_md5 == MakeRar.file_md5(new_path):
                    MakeRar.force_delete(file_path)
                else:
                    MakeRar.force_delete(new_path)
                    os.rename(file_path, new_path)
            else:
                os.rename(file_path, new_path)
        else:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)

    @staticmethod
    def force_delete(file_path):
        if os.path.isdir(file_path):
            try:
                shutil.rmtree(file_path)
            except Exception as e:
                func_name = sys._getframe().f_code.co_name
                error_lines = sys._getframe().f_lineno
                error = f"{error_lines}: {func_name} {e}"
                write_Error(error)
                command = f"rar a -ep1 -df delete.rar {file_path}"
                if excu_command(command):
                    os.remove(r"delete.rar")
        else:
            try:
                os.remove(file_path)
            except Exception as e:
                error = f"{__name__}-->:{e}"
                write_Error(error)
                command = f"rar a -ep1 -df delete.rar {file_path}"
                if excu_command(command):
                    os.remove(r"delete.rar")

    @staticmethod
    def rar_co(target_path, dist_path, password="infected"):
        command = f"rar a -ep1 -df -inul -p{password} {target_path} {dist_path}"
        try:
            check_output(command, shell=True)
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)

    def files_split(self, folder, split_size=1024 * 1024 * 500):
        total_size = 0
        files_list = self.file_path_list(folder)
        files_dict = {}
        for file_path in files_list:
            files_dict[file_path] = os.path.getsize(file_path)
            total_size += os.path.getsize(file_path)
        samples_dict = {}
        samples_key = 0
        samples_values = []
        current_size = 0

        for file_path, file_size in files_dict.items():
            if current_size <= split_size <= total_size:
                current_size += file_size
                samples_values.append(file_path)
                samples_dict[samples_key] = samples_values
                total_size -= file_size
            elif current_size > split_size:
                samples_key += 1
                samples_values = []
                current_size = 0
                current_size += file_size
                samples_values.append(file_path)
                samples_dict[samples_key] = samples_values
                total_size -= file_size
            elif split_size > total_size:
                samples_values.append(file_path)
                samples_dict[samples_key] = samples_values
        return samples_dict

    def organize_files(self, folder):
        # 整理文件, 重命名
        for file_path in self.file_path_list(folder):
            new_name = f"{self.file_md5(file_path)}.vir"
            if self.rename_by(file_path, new_name) is False:
                self.deal_file(file_path)

    def deal_file(self, all_path, password="infected"):
        file_dir = os.path.dirname(__file__)
        temp_path = os.path.join(file_dir, r"temp")
        if os.path.exists(temp_path) is False:
            os.makedirs(temp_path)
        try:
            for file_path in all_path:  # 解压到临时目录
                command = f"7z x -tzip -p{password} -y \"{file_path}\" -o\"{temp_path}\""
                if file_path[-4:] == ".zip" and excu_command(command):

                    self.rename_by(file_path, f"[已交换]{os.path.basename(file_path)}")
            self.deal_fodler(temp_path)
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)
        else:
            self.force_delete(temp_path)

    def deal_fodler(self, folder):
        try:
            self.organize_files(folder)
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            error_lines = sys._getframe().f_lineno
            error = f"{error_lines}: {func_name} {e}"
            write_Error(error)
        else:
            sample_dict = self.files_split(folder)
            last_upload_date = self.get_last_upload_date()
            folder_name = last_upload_date + datetime.timedelta(days=1)
            if datetime.datetime.weekday(folder_name) == 5:
                folder_name += datetime.timedelta(days=2)
            for values in sample_dict.values():
                sample_name = datetime.datetime.strftime(folder_name, "samples-%Y%m%d")
                sample_path = os.path.join(upload_dir, sample_name)
                if os.path.exists(sample_path) is False:
                    os.makedirs(sample_path)
                for file_path in values:
                    shutil.move(file_path, sample_path)
                folder_name += datetime.timedelta(days=1)
                if datetime.datetime.weekday(folder_name) == 5:
                    folder_name += datetime.timedelta(days=2)
        for file_path in self.file_path_list(upload_dir):
            if os.path.isdir(file_path):
                self.rar_co(file_path, file_path)


# if __name__ == "__main__":
    MakeRar()
