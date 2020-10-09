from sys import argv, exit

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QHBoxLayout, \
    QVBoxLayout, QGridLayout



class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.set_window()

    def set_window(self):
        # 静态设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip("窗口提示文字")
        #  静态图标
        icon = QIcon(r"/First/Base/ico.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("窗口标题")
        self.setGeometry(100, 100, 500, 500)
        # 插件布局
        self.window_layout()
        #  居中显示
        self.center()
        # 显示窗口
        self.show()

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_set_test(self):
        button = QPushButton("按钮设置", self)
        # 设置提示文字
        button.setToolTip("按钮提示文字")
        button.setFixedWidth(100)
        return button

    def closeEvent(self, event):
        box_attr = ("Message", "Are you sure to quit?")
        box = QMessageBox.question(self, *box_attr, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # 最后一个参数是默认按钮，这个是默认的按钮焦点。
        event.accept() if box == QMessageBox.Yes else event.ignore()

    def window_layout(self):
        # 绝对布局
        """
        # 显示默认尺寸
        button = QPushButton("按钮", self)
        button.resize(button.sizeHint())
        # 移动窗口的位置
        button.move(10, 10)
        """
        # 框布局
        '''
        QHBoxLayout：水平布局，在水平方向上排列控件，即：左右排列。 
        QVBoxLayout：垂直布局，在垂直方向上排列控件，即：上下排列。
        addStretch()  默认值为0 ， 水平方向，拉伸因子将按钮排列在右侧
        '''
        '''
        button_1 = QPushButton("按钮1", self)
        button_2 = QPushButton("按钮2", self)
        hb = QHBoxLayout()
        hb.addStretch(0)
        hb.addWidget(button_1)
        hb.addWidget(button_2)
        vb = QVBoxLayout()
        vb.addStretch(0)
        vb.addLayout(hb)
        self.setLayout(vb)
        '''
        # 表格布局
        """
        addWidget(QWidget Widget,int row,int col,int alignment=0)	
        给网格布局添加部件，设置指定的行和列，起始位置的默认值为（0,0） alignment：对齐方式
        """
        grid = QGridLayout()
        self.setLayout(grid)
        button_1 = QPushButton("button_1", self)
        button_2 = QPushButton("button_2", self)
        button_3 = QPushButton("button_3", self)
        button_4 = QPushButton("button_4", self)
        button_5 = QPushButton("button_5", self)
        button_6 = QPushButton("button_6", self)
        button_7 = QPushButton("button_7", self)
        button_1.clicked.connect(self.button_func)
        grid.addWidget(button_1, 0, 0)
        grid.addWidget(button_2, 1, 0)
        grid.addWidget(button_3, 1, 1)
        grid.addWidget(button_4, 2, 0)
        grid.addWidget(button_5, 2, 1)
        grid.addWidget(button_6, 2, 2)
        grid.addWidget(button_7, 3, 1, 1, 2)  # 第3行第1列，跨越1行2列

    def button_func(self):
        sender = self.sender()
        sender.text() + "a"
        print("1")

if __name__ == "__main__":
    app = QApplication(argv)
    a = Main()
    """
    Because if you don't store a reference to an object, 
    it is discarded and its memory released for reuse immediately.
    """
    exit(app.exec_())
