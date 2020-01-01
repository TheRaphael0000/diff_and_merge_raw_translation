import sys
import random
import os

from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QListWidget
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPixmap


class ImageViewer(QWidget):
    def load_files(self, x):
        self.folder = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))

        self.select.setText(self.folder)
        fs = os.listdir(self.folder)

        while self.list.count() > 0:
            self.list.takeItem(0)

        for f in fs:
            self.list.addItem(f)

    def load_image(self, item):
        filename = item.text()
        path = os.path.join(self.folder, filename)
        img = QPixmap(path)
        w = self.img.width()
        h = self.img.height()
        self.img.setPixmap(img.scaled(w, h, Qt.KeepAspectRatio))
        print(path)

    def __init__(self, str_folder, str_validate):
        QWidget.__init__(self)

        self.folder = None

        self.v = QVBoxLayout()
        self.h = QHBoxLayout()
        self.select = QPushButton(str_folder)
        self.img = QLabel()
        self.validate = QPushButton(str_validate)
        self.img.setMinimumSize(600, 300)
        # self.img.setMinimumSize(100, 100)
        # self.img.setScaledContents(True)
        self.list = QListWidget()
        self.setMaximumWidth(400)

        self.h.addWidget(self.list)
        self.h.addWidget(self.img)

        self.v.addWidget(self.select)
        self.v.addLayout(self.h)
        self.v.addWidget(self.validate)

        self.setLayout(self.v)

        self.select.clicked.connect(self.load_files)
        self.list.currentItemChanged.connect(self.load_image)


class MyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.h = QHBoxLayout()
        self.v = QVBoxLayout()

        self.A = ImageViewer("Select input folder A", "Add")
        self.B = ImageViewer("Select input folder B", "Add")
        self.C = ImageViewer("Select output folder", "Remove")

        self.v.addWidget(self.A)
        self.v.addWidget(self.B)

        self.h.addLayout(self.v)
        self.h.addWidget(self.C)

        self.setLayout(self.h)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
