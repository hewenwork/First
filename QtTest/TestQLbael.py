# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:TestQLbael.py
@time:2020/09/29
"""

from sys import argv, exit
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage, QMouseEvent, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QSystemTrayIcon, QAction, QMenu, QPushButton
from PyQt5.QtCore import Qt, QPoint


class Main(QWidget):
    _startPos = None
    _endPos = None
    _isTracking = False

    def __init__(self):
        super(Main, self).__init__()
        self.window_set()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.window_grid()
        self.show()

    def window_set(self):
        icon = QIcon(r"C:\Users\hewen\Desktop\Icon\IU.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("GUI TEST")
        palette = QPalette()
        image = QImage(r"C:\Users\hewen\Desktop\51.jpg")
        palette.setBrush(QPalette.Background, QBrush(image))
        self.setPalette(palette)
        self.setFixedSize(image.size().width(), image.size().height())
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框, 也就是没有关闭按钮

    def window_grid(self):
        self.label_show()
        self.button_exit()

    def label_show(self):
        def label_1_func():
            print("aa")

        label_1 = QLabel(self)
        label_1.setText("<a href='https://www.baidu.com'>点击查看更多</a>")
        # label_1.setAutoFillBackground(True)
        label_1.setOpenExternalLinks(True)  # 允许联网
        self.grid.addWidget(label_1, 0, 0, Qt.AlignLeft)
        label_1.linkActivated.connect(label_1_func)

    def button_exit(self):


        button = QPushButton(self)
        button.setText("")
        button.setFixedWidth(50)
        self.grid.addWidget(button, 0, 1, Qt.AlignTop)
        button.clicked.connect(self.close)
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(1)
        button.setGraphicsEffect(op)
        button.setIcon(QIcon(r"C:\Users\hewen\Desktop\Icon\IU.ico"))

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


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    exit(app.exec_())
