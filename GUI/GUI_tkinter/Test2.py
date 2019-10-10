# encoding = utf-8
# @Author: Hewen
# @Time: 10/8/2019 1:40 PM
# @File: Test2.py
from tkinter import *


class Test2:

    def __init__(self):
        self.windows = Tk()
        canvas = Canvas(self.windows, bg="white")
        image = PhotoImage(file=r"C:\Users\hewen\Desktop\background.png")
        canvas.create_image(250, 0, image=image)
        canvas.pack()
        self.windows.mainloop()


if __name__ == "__main__":
    Test2()
