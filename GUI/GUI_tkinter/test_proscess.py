import datetime
import os
import time
from tkinter import *

import requests


class TestP:

    @classmethod
    def windows_set(cls):
        window = Tk()
        # 图标
        # window.iconbitmap(r"C:\Users\hewen\Desktop\ico.ico")
        # 显示位置
        window.geometry("+600+100")
        # 最小/大窗口
        window.minsize(width=600, height=600)
        window.maxsize(width=600, height=600)
        # 标题
        window.title(u"窗口标题")
        return window

    def change(self):
        # self.button["state"] = "disable"
        if self.button_text.get() == "开始":
            self.button_text.set("暂停")
            for i in range(1, 100):
                if self.button_text.get() == "暂停":
                    time.sleep(0.1)
                    self.window.update()
                    self.process.set("%s" % (i + 1))
                    self.canvas.coords(self.canvas.create_rectangle(5, 5, 6 + i, 25, outline="blue", width=3))
                else:
                    break
            self.process.set("Complete")
        else:
            self.button_text.set("开始")
            self.process.set("Push")
            time.sleep(1)

        # self.button["state"] = "normal"

    def label_set(self):
        label = Label(self.window, textvariable=self.process)
        return label

    def button_one_set(self):
        self.button_text.set("单次下载")
        button = Button(self.window, textvariable=self.button_text, command=self.change)
        return button

    def button_cycle_set(self):
        self.button_text.set("循环下载")
        button = Button(self.window, textvariable=self.button_text, command=self.change)
        return button

    def frame_set(self):
        frame = Frame(self.window)
        return frame

    def canvas_set(self):
        canvas = Canvas(self.frame)
        # canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=3)
        # canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
        return canvas

    def __init__(self):
        self.window = self.windows_set()
        self.label_url = Label(self.window, text="下载地址")
        self.label_url_show = Label(self.window, textvariable=None)
        # self.process = StringVar()
        # self.process.set("Hello")
        # self.label = self.label_set()
        # self.label.place(x=15, y=10, width=50, height=12)
        # self.button_text = StringVar()
        # self.button = self.button_one_set()
        # self.button.place(x=550, y=20, width=40, height=40)
        # self.frame = self.frame_set()
        # self.frame.place(x=30, y=40, width=200, height=10)
        # self.canvas = self.canvas_set()
        # self.canvas.place(x=1, y=1, width=200, height=10)
        self.window.mainloop()


class Urlhaus:

    def __init__(self):
        self.base_dir = os.getcwd()
        self.dist_dir = r"\\192.168.1.39\f\Auto"
        self.session = self.get_session()
        self.download_date = self.get_download_date()

    @staticmethod
    def get_session():
        user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
        headers = {"User-Agent": user_agent}
        session = requests.session()
        session.headers.update(headers)
        return session

    @staticmethod
    def get_download_date():
        today = datetime.datetime.today()
        date_interval = datetime.timedelta(days=1)
        download_day = today - date_interval
        return download_day.strftime("%Y-%m-%d")

    def write_log(self, result, download_url):
        log_path = os.path.join(self.base_dir, "urlhaus.log")
        data = "%s: download %s %s\n" % (self.download_date, result, download_url)
        if os.path.exists(log_path):
            with open(log_path, "r+")as file:
                old_data = file.read()
                file.seek(0, 0)
                file.write(data + old_data)
        else:
            with open(log_path, "a+")as file:
                file.write(data)

    def write_sample(self, file_path, download_url):
        if os.path.exists(file_path):
            return "Successful"
        else:
            try:
                file_size = 0
                response = self.session.get(url=download_url, stream=True)
                file_total_size = int(response.headers["content-length"])
                with open(file_path, "wb")as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                        file_size += 1024
                        download_process = int(file_size/file_total_size*100)
                        print("\rDownload %s %s%%" % ("#"*download_process, download_process), end="")
                return "Successful"
            except requests.RequestException as e:
                print(e)
                return "Failed"

    def start_download(self):
        file_name = "%s.zip" % self.download_date
        file_path = os.path.join(self.base_dir, "urlhaus[infected]%s" % file_name)
        download_url = "https://urlhaus-api.abuse.ch/downloads/%s" % file_name
        download_result = self.write_sample(file_path, download_url)
        try:
            command = "copy %s %s" % (file_path, self.dist_dir)
            os.system(command)
        except OSError as e:
            print(e)
        self.write_log(download_result, download_url)


if __name__ == "__main__":
    TestP()
