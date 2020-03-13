import os
import sys
import locale
import ctypes
import psutil
from tkinter.ttk import Combobox
from tkinter import Button, Tk, Scale, StringVar, Entry, Label

dll_kernel = ctypes.windll.kernel32
geo = dll_kernel.GetSystemDefaultUILanguage()
lang = locale.getdefaultlocale()[0]
print(lang)

disk_c_info = psutil.disk_usage(psutil.disk_partitions()[0][0])
size_mb = 1024 * 1024
size_gb = 1024 * 1024 * 1024
Total_size = disk_c_info[0] / size_mb
Used_size = disk_c_info[1] / size_mb
Free_size = disk_c_info[2] / size_mb
print(Total_size, Free_size)


class Ui:

    def __init__(self):
        self.app = Tk()
        size_value = StringVar()
        self.scale = Scale(self.app, from_=0, to=Free_size)
        self.enter = Entry(self.app)
        self.enter.insert(0, f"{Free_size} MB")
        self.label = Label(self.app, text="磁盘空间剩余")
        self.combobox = Combobox(self.app, textvariable=StringVar)
        self.combobox["values"] = [str(i) for i in range(1, int(Free_size))]
        self.combobox.current(0)
        self.scale.pack()
        self.combobox.pack()
        self.enter.pack()
        self.app.mainloop()


if __name__ == "__main__":
    # Ui()
    # print(41.3 * 1024 *1024 *1024)
    for i in range(1, 101):
        print(f"{i}")