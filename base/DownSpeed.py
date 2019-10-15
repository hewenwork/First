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
            self.alone(self.url)
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

    def alone(self, url):
        try:
            content = requests.get(url).content
        except Exception as e:
            print(e)
            return
        else:
            self.file.write(content)


class DownloadGui:

    def __init__(self):
        self.window = self.main()
        self.button = self.button_download()
        self.url_in = self.url_input()
        self.url_in.place(relx=0.1, rely=0.1, anchor=NW, x=10, y=20)
        self.button.place(relx=0.2, rely=0.1)

        self.window.mainloop()

    @staticmethod
    def main():
        window = Tk()
        window.title(u"肖尤花专用IMF下载器")
        window.geometry("600x400+100+100")
        window.attributes("-topmost", True)
        return window

    def button_download(self):
        button = Button(self.window)
        button["text"] = u"下载"
        button["state"] = "disabled"
        button["command"] = self.button_func
        return button

    def button_func(self):
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
            thread = threading.Thread(target=DownSpeed, args=(file_path, download_url))
            thread.run()
            self.framebg()
        else:
            messagebox.showwarning(title=u"警告", message=u"下载链接不对, 请重新输入")

    def url_input(self):
        text = Entry(self.window)
        text["justify"] = "left"
        text["width"] = 100
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

    def framebg(self):
        self.x = StringVar()
        self.frame = Frame(self.window)
        self.frame.place(relx=0.1, rely=0.1, anchor=NW, x=10, y=20)
        self.canvas = Canvas(self.frame, width=120, height=30, bg="yellow")
        self.canvas.grid(row=0, column=0)
        out_rec = self.canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=1)
        fill_rec = self.canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")

        # def processbar(self, now_schedule, all_schedule):
        self.canvas.coords(fill_rec, (5, 5, 6 + (1 / 100) * 100, 25))
        self.window.update()
        self.x.set(str(round(1 / 100 * 100, 2)) + '%')
        if round(1 / 100 * 100, 2) == 100.00:
            self.x.set("完成")


if __name__ == "__main__":
    DownloadGui()
