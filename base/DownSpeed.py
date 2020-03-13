import os
import asyncio
import aiohttp
import requests
import threading
from tkinter import *
from faker import Faker
from tkinter import filedialog, messagebox


class DownSpeed:

    def __init__(self, file_path, download_url, auth=None):
        self.headers = {"Accept-Encoding": "gzip, deflate, br", "User-Agent": Faker().user_agent()}
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.chunk_size = 1024 * 1024
        self.task = []
        self.url = download_url
        self.file = file_path
        response = self.session.get(self.url, stream=True, auth=auth)
        if "Accept-Ranges" in response.headers.keys():
            aiohttp.BasicAuth = auth
            self.total_size = int(response.headers["Content-Length"])
            self.chunk_num = int(self.total_size / self.chunk_size) + 1
            self.loop = asyncio.get_event_loop()
            self.loop.run_until_complete(self.get_total_size())
            self.loop.close()
        else:
            self.alone_direct(self.url)
        self.file.close()

    async def get_total_size(self):
        async with aiohttp.ClientSession() as session:
            start_size = 0
            for i in range(self.chunk_num):
                end_size = self.chunk_size + start_size
                if self.chunk_num - i == 1:
                    end_size = self.total_size
                self.task.append(self.loop.create_task(self._star(start_size, end_size, session)))
                start_size = end_size + 1
            await asyncio.wait(self.task)

    async def _star(self, start_size, end_size, session):
        self.headers["range"] = f"bytes={start_size}-{end_size}"
        async with session.get(self.url, headers=self.headers)as chunk:
            self.continue_download = False
            content = await chunk.read()
            self.file.seek(start_size, 0)
            self.file.write(content)
            self.file.flush()

    def alone_direct(self, url):
        try:
            content = requests.get(url).content
        except Exception as e:
            print(e)
            return
        else:
            self.file.write(content)

    def alone_chunk(self, url, command):
        try:
            for chunk in requests.get(url, stream=True).iter_content(chunk_size=8192):
                self.file.write(chunk)
                command()
        except:
            print(1)


class DownloadGui:

    def __init__(self):
        self.window = self.main()
        self.button = self.button_download()
        self.url_in = self.url_input()
        self.url_in.place(x=10, y=20)
        self.button.place(x=10, y=40)
        self.window.mainloop()

    @staticmethod
    def alone_chunk(url, command):
        try:
            file = open(r"C:\Users\hewen\Desktop\2015.exe", "wb")
            total = int(requests.get(url, stream=True).headers["content-length"])
            content_size = 0
            for chunk in requests.get(url, stream=True).iter_content(chunk_size=8192):
                file.write(chunk)
                content_size += 8192
                command(round(content_size / total, 2))
            file.close()
        except Exception as e:
            print(e)

    @staticmethod
    def main():  # 主界面
        window = Tk()
        window.title(u"直链下载")
        window.geometry("600x400+100+100")
        window.attributes("-topmost", True)
        return window

    def button_download(self):  # 下载按钮
        button = Button(self.window)
        button["text"] = u"下载"
        button["state"] = "disabled"
        button["command"] = self.button_func
        return button

    def button_func(self):  # 按钮功能
        download_url = self.url_in.get()
        if ":/" in download_url:
            self.button["state"] = "disable"
            option = {
                "filetypes": [('all files', '.*'), ('text files', '.txt')],
                "title": u"保存位置",
                "initialdir": r"C:\Users\hewen\Desktop\小工具",
                "initialfile": download_url.split("/")[-1]
            }
            file_path = filedialog.asksaveasfile(mode="wb", **option)
            thread = threading.Thread(target=self.alone_chunk, args=(download_url, self.framebg))
            thread.run()
        else:
            messagebox.showwarning(title=u"警告", message=u"下载链接不对, 请重新输入")

    def url_input(self):  # url输入框
        option = {
            "justify": "left",
            "width": 80
        }
        text = Entry(self.window, **option)
        text.insert(0, u"请在这里输入或粘贴要下载的链接, 按下载按钮开始下载")
        text.bind('<FocusIn>', self.on_entry_click)
        return text

    def on_entry_click(self, event):
        if self.url_in.get() == u"请在这里输入或粘贴要下载的链接, 按下载按钮开始下载":
            self.url_in.delete(0, "end")
            self.url_in.insert(0, "")
            self.url_in.config(fg="black")
            self.button["state"] = "active"

    def on_focusout(self, event):
        if self.url_in.get() == "":
            self.url_in.insert(0, u"请在这里输入或粘贴要下载的链接, 按下载按钮开始下载")
            self.url_in.config(fg="blue")
        else:
            self.button["state"] = "active"

    def framebg(self, process):
        frame = Frame(self.window)
        label = Label(self.window, text=u"下载进度%s%%" % process * 100 if process != 1 else u"下载完成")
        frame.place(x=10, y=60)
        label.place(x=10, y=90)
        option = {
            "width": 200,
            "height": 30,
            "confine": False
        }
        canvas = Canvas(frame, **option)
        canvas.create_rectangle(5, 5, 100, 25, outline="blue", width=1)
        canvas.create_rectangle(5, 5, process * 100, 25, outline="blue", width=1, fill="blue")
        canvas.grid()


if __name__ == "__main__":
    DownloadGui()
