from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        hlay = QtWidgets.QHBoxLayout(central_widget)

        self.overview_widget = QtWidgets.QWidget()
        self.fill_overview()
        self.level_widget = QtWidgets.QWidget()
        self.fill_level()
        self.tape_measure_widget = QtWidgets.QWidget()
        self.fill_tape_measure()
        self.theodolite_widget = QtWidgets.QWidget()
        self.fill_theodolite()

        self.list_widget = QtWidgets.QListWidget()

        self.slay = QtWidgets.QStackedLayout()
        hlay.addWidget(self.list_widget)
        hlay.addLayout(self.slay)
        hlay.setStretch(0, 0)
        hlay.setStretch(1, 1)

        self.list_widget.currentRowChanged.connect(self.slay.setCurrentIndex)

        for w, text in (
            (self.overview_widget, "OVERVIEW"),
            (self.level_widget, "LEVEL"),
            (self.tape_measure_widget, "TAPE MEASURE"),
            (self.theodolite_widget, "THEODOLITE"),
        ):
            self.slay.addWidget(w)
            self.list_widget.addItem(text)

    def fill_overview(self):
        hlay = QtWidgets.QVBoxLayout(self.overview_widget)
        hlay.addWidget(
            QtWidgets.QLabel("Overview", alignment=QtCore.Qt.AlignCenter)
        )
        self.overview_widget.setStyleSheet("background-color:green;")

    def fill_level(self):
        hlay = QtWidgets.QVBoxLayout(self.level_widget)
        hlay.addWidget(
            QtWidgets.QLabel("Level", alignment=QtCore.Qt.AlignCenter)
        )
        self.level_widget.setStyleSheet("background-color:blue;")

    def fill_tape_measure(self):
        hlay = QtWidgets.QVBoxLayout(self.tape_measure_widget)
        hlay.addWidget(
            QtWidgets.QLabel("Tape Measure", alignment=QtCore.Qt.AlignCenter)
        )
        self.tape_measure_widget.setStyleSheet("background-color:red;")

    def fill_theodolite(self):
        hlay = QtWidgets.QVBoxLayout(self.theodolite_widget)
        hlay.addWidget(
            QtWidgets.QLabel("Theodolite", alignment=QtCore.Qt.AlignCenter)
        )
        self.theodolite_widget.setStyleSheet("background-color:gray;")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 240)
    w.show()
    sys.exit(app.exec_())