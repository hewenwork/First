# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:MakeBug.py
@time:2020/09/30
"""

from sys import argv, exit
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage, QMouseEvent, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QSystemTrayIcon, QAction, QMenu, QPushButton, \
    QLayout
from PyQt5.QtCore import Qt, QPoint, QSize


class Window(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super(Window, self).__init__()
        image_icon = QIcon(r"C:\Users\hewen\Desktop\Icon\ico.ico")
        image_bg = QImage(r"C:\Users\hewen\Desktop\image\background.jpg")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(image_bg))
        window_title = "Test For All"
        window_width = image_bg.size().width()
        window_height = image_bg.size().height()
        self.setPalette(palette)
        self.setWindowIcon(image_icon)
        self.setWindowTitle(window_title)
        self.setFixedSize(window_width, window_height)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框, 也就是没有关闭按钮

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


class Main(Window):
    grid = QGridLayout()

    def __init__(self):
        super(Main, self).__init__()
        self.widget_layout()
        self.show()

    def widget_layout(self):
        self.label_show()
        self.button_exit()
        # self.button_asc()
        self.setLayout(self.grid)

    def label_show(self):
        def label_1_func():
            print("aa")

        label_1 = QLabel(self)
        label_text = "<a href='https://www.baidu.com'>点击查看更多</a>"
        label_1.setText(label_text)
        label_1.setOpenExternalLinks(True)  # 允许联网
        self.grid.addWidget(label_1, 0, 0, Qt.AlignTop)
        label_1.linkActivated.connect(label_1_func)

    def button_exit(self):
        image = QPixmap(QImage(r"C:\Users\hewen\Desktop\Image\images\btn_mini_press.png"))
        ico = image.scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        button = QPushButton(self)
        button.setIcon(QIcon(ico))
        button.setIconSize(QSize(30, 30))
        button.setFixedSize(30, 30)
        button.setStyleSheet("QPushButton{border-image: url(C:/Users/hewen/Desktop/Image/1.jpg)}"
                             "QPushButton:hover{border-image: url(C:/Users/hewen/Desktop/Image/1.jpg)}")

        self.grid.addWidget(button, 0, 1, Qt.AlignTop)
        button.clicked.connect(self.close)
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(1)
        button.setGraphicsEffect(op)

    def button_asc(self):
        image_asc = QIcon(r"C:\Users\hewen\Desktop\Image\images\btn_mini_press.png")
        button = QPushButton(self)
        button.setFixedWidth(50)
        button.clicked.connect(self.close)
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(1)
        button.setGraphicsEffect(op)
        button.setIcon(image_asc)
        self.grid.addWidget(button, 0, 2, Qt.AlignTop)


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    exit(app.exec_())
