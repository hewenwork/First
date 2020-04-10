# encoding = utf-8
# @Author: Hewen
# @Time: 10/25/2019 3:36 PM
# @File: MakeApp.py
import os
import shutil
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from PyInstaller import __main__


class MakeApp:

    def __init__(self):
        try:
            tkinter.Tk().withdraw()
            file_path = filedialog.askopenfile().name
            if os.path.exists(file_path):
                self.make(file_path)
        except AttributeError:
            messagebox.showwarning(message=u"未选择任何py文件")
            exit()

    @staticmethod
    def make(file_path, file_name=None):
        if file_name is None:
            file_name = os.path.basename(file_path).split(".")[0]
        current_dir = os.path.dirname(__file__)
        temp_dir = os.path.join(current_dir, r"justonemin")
        option = [
            f"--name={file_name}",
            f"--distpath={current_dir}",
            f"--specpath={temp_dir}",
            f"--workpath={temp_dir}",
            # "--noconsole",
            "--onefile",
            "--clean",
            "--noconfirm",
            "--log-level=ERROR",
            "--paths=F:\Workspace\First",
            # "--exclude-module pywin32-stypes",
            # f"--additional-hooks-dir f:\\python\\lib\\site-packages",
            # '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
            # '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
            file_path
        ]
        ico = r"ico.ico"
        if os.path.exists(ico):
            ico_path = os.path.abspath(r"ico.ico")
            option.insert(0, f"--icon={ico_path}")
        try:
            __main__.run(option)
        except Exception as e:
            messagebox.showwarning(message=e)
            exit()
        else:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    MakeApp()
