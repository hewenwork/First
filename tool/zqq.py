# encoding = utf-8
import os
import shutil
import tkinter
import chardet
import hashlib
import datetime
import configparser
import tkinter.messagebox
from pynput.keyboard import Listener
from subprocess import check_output, SubprocessError


class Zqq:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.config_file = self.get_setting_file(file_path=r"main.ini")
        self.parser.read(self.config_file, encoding=self.get_encoding(self.config_file))
        self.init_net()
        with Listener(on_release=self.release) as self.listener:
            self.listener.join()

    @staticmethod
    def log_error(error):
        with open("Error.log", "a+", encoding="utf-8")as file:
            line = "{}:{}\n".format(datetime.datetime.now(), error)
            file.writelines(line)

    @staticmethod
    def warning_info(title, message):
        warning = tkinter.Tk()
        warning.wm_attributes('-topmost', 1)
        warning.withdraw()
        tkinter.messagebox.showerror(title=title, message=message)
        warning.destroy()

    def get_file_md5(self, file_path):
        try:
            with open(file_path, "rb")as md5_file:
                md5_con = hashlib.md5()
                md5_con.update(md5_file.read())
                md5_result = str(md5_con.hexdigest())
                return md5_result.upper()
        except OSError as e:
            self.log_error(e)

    @staticmethod
    def get_encoding(file_path):
        with open(file_path, "rb")as file:
            encoding = chardet.detect(file.read())["encoding"]
        if encoding is None:
            encoding = "utf-8"
        return encoding

    def get_setting_file(self, file_path):
        if os.path.exists(file_path) is False:
            title = u"警告"
            message = u"你的配置文件main.ini不存在. 请检查"
            self.warning_info(title, message)
            self.log_error(message)
        else:
            return file_path

    def init_net(self):
        user = self.parser.get("login", "user")
        password = self.parser.get("login", "password")
        cloud_path = "\\\\192.168.1.254\\部门共享\\TEST\\贺文(HW)"
        if os.path.exists(cloud_path)is False:
            command = "net use \"{}\" {} /user:{}".format(cloud_path, user, password)
            try:
                check_output(command, shell=True)
            except SubprocessError as e:
                self.log_error(e)
                self.warning_info("错误", "没有链接254")

    def release(self, key):
        try:
            if key == key.f8:
                title = u"注意"
                message = u"开始同步您的文件夹"
                self.warning_info(title, message)
                self.get_all_path()
                title = u"注意"
                message = u"文件夹同步完成"
                self.warning_info(title, message)
            elif key == key.f9:
                title = u"注意"
                message = u"将退出同步工具"
                self.warning_info(title, message)
                self.listener.stop()
            elif key == key.ctrl_1:
                print(1111)
        except AttributeError as e:
            self.log_error(e)

    def get_all_path(self):
        for cloud_key, cloud_value in self.parser.items("254"):
            local_value = self.parser.get("local", cloud_key)
            if os.path.exists(local_value) and os.path.exists(cloud_value):
                for cloud_file_name in os.listdir(cloud_value):
                    cloud_file_path = os.path.join(cloud_value, cloud_file_name)
                    local_file_path = os.path.join(local_value, cloud_file_name)
                    if os.path.exists(local_file_path)is False:
                        shutil.copy(cloud_file_path, local_value)
                    else:
                        if os.path.getsize(local_file_path) != os.path.getsize(cloud_file_path):
                            shutil.copy(cloud_file_path, local_value)
                            print(cloud_file_path)
                    # if cloud_file_name not in os.listdir(local_value):
                    #     shutil.copy(cloud_file_path, local_value)
                    # else:
                    #     if self.get_file_md5(local_file_path) != self.get_file_md5(cloud_file_path):
                    #         shutil.copy(cloud_file_path, local_value)
            else:
                message = "不存在本地文件夹或254不存在指定的文件夹"
                self.warning_info("Notice", message)
                self.log_error(message)


if __name__ == "__main__":
    Zqq()
