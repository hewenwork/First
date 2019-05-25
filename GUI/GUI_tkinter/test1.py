# coding = utf-8
import os
import base64
import requests
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Combobox
base_dir = r"C:\Users\hewen\Desktop\20190524"
year = StringVar


class TestGui:

    def __init__(self):
        self.app = self.init_window()
        self.label = self.label_p()
        self.label.place(x=15, y=10, width=50, height=20)
        self.combobox = self.combobox()
        self.combobox.place(x=15, y=30, width=50, height=20)
        self.button_start = self.button_start()
        # self.button_start.config(command=TestCommand.command_button1)
        self.button_start.place(x=550, y=20, width=40, height=40)
        # self.canvas_download()
        self.app.mainloop()

    @staticmethod
    def init_window():
        window = Tk()
        # 图标
        window.iconbitmap(r"C:\Users\hewen\Desktop\ico.ico")
        # 显示位置
        window.geometry("+600+100")
        # 最小/大窗口
        window.minsize(width=600, height=600)
        window.maxsize(width=600, height=600)
        # 标题
        window.title(u"窗口标题")
        return window

    def button_start(self):
        bt_start = Button(self.app)
        bt_font = Font(family="Helvetica", size=6, weight="bold", slant="italic")
        bt_start["height"] = "3"
        bt_start["width"] = "3"
        bt_start["bg"] = "orange"  # 背景颜色
        bt_start["foreground"] = "red"  # 文字颜色
        bt_start["activebackground"] = "green"  # 当鼠标按下时，按钮的背景色
        bt_start["activeforeground"] = "yellow"  # 当鼠标按下时，文本的颜色
        bt_start["text"] = u"开始按钮"
        bt_start["font"] = bt_font
        bt_start["padx"] = 1
        bt_start["relief"] = "raised"
        bt_start["cursor"] = "heart"
        bt_start["command"] = None
        # bt_start["state"] = "disable"
        return bt_start

    def canvas_download(self):
        canvas = Canvas(self.app)
        # canvas.create_rectangle(2,2,180,27,width = 1,outline = "black")
        # canvas["bg"] = "red"
        # canvas["bd"] = 3
        # canvas.place(x=40, y=20, width=500, height=40)

    def combobox(self):
        combobox = Combobox(self.app)
        combobox["justify"] = "left"
        combobox["state"] = "readonly"
        combobox["values"] = ["IU", "ISU", "IMF"]
        combobox.current(1)
        return combobox

    def label_p(self):
        label = Label(self.app)
        label["text"] = u"产品选择"
        return label


class GetBugreport:

    @staticmethod
    def get_product():
        product_name = input(u"请输入产品名对应的数字\n1:IU\n2:IMF \n3:ISU\n")
        product_dict = {
            "1": "iu",
            "2": "imf",
            "3": "su",
            "4": "asc",
            "5": "ascu",
            "6": "db",
            "7": "sd"
        }
        product = product_dict[product_name]
        return product

    @staticmethod
    def get_date():
        download_date = input(u"请输入下载日期如2019-05-14\n")
        return download_date

    @staticmethod
    def get_report():
        download_date = GetBugreport.get_date()
        product = GetBugreport.get_product()
        download_dir = os.path.join(base_dir, r"%s\%s" % (product, download_date))
        if os.path.exists(download_dir) is False:
            os.makedirs(download_dir)
        url = "http://ascstats.iobit.com/other/bugReport/json_today/json_today.php"
        params = {
            "table": "%s_bugreport_v2" % product,
            "date": download_date
        }
        response = requests.get(url=url, params=params)
        return_size = int(response.headers["content-length"])
        if return_size <= 1024:
            print("No Data")
        else:
            for user_num in response.json():
                file_name = user_num["id"] + user_num["email"] + ".zip"
                file_path = os.path.join(download_dir, file_name)
                with open(file_path, "wb")as file:
                    bugcontent = base64.b64decode(user_num["bugcontent"])
                    file.write(bugcontent)


if __name__ == "__main__":
    TestGui()
