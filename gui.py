import sys
import os

from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QListWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

from diff_and_merge import DiffMerge


class Picker(QWidget):
    def __init__(self, str_folder, img):
        QWidget.__init__(self)

        self.setMaximumWidth(400)

        self.folder = None
        self.files = []
        self.img = img

        self.v = QVBoxLayout()
        self.select = QPushButton(str_folder)
        self.list = QListWidget()

        self.v.addWidget(self.select)
        self.v.addWidget(self.list)

        self.setLayout(self.v)

        self.list.currentItemChanged.connect(self.load_image)

    def load_image(self, item):
        filename = item.text()
        path = os.path.join(self.folder, filename)
        img = QPixmap(path)
        w = self.img.width()
        h = self.img.height()
        self.img.setPixmap(img.scaled(w, h, Qt.KeepAspectRatio))

    def update_files(self, files):
        self.files = files
        while self.list.count() > 0:
            self.list.takeItem(0)

        for f in self.files:
            self.list.addItem(f)


class InputPicker(Picker):

    def __init__(self, str_folder, img):
        super().__init__(str_folder, img)
        self.select.clicked.connect(self.load_folder)

    def load_folder(self, x):
        self.folder = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))

        self.select.setText(self.folder)
        self.update_files(os.listdir(self.folder))


class OutputPicker(Picker):

    def __init__(self, str_folder, img):
        super().__init__(str_folder, img)
        self.select.clicked.connect(self.load_folder)

    def load_folder(self, x):
        self.folder = str(QFileDialog.getExistingDirectory(
            self, "Select Directory"))

        self.select.setText(self.folder)


class MyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.h = QHBoxLayout()
        self.v = QVBoxLayout()

        self.img = QLabel()
        self.img.setFixedWidth(560)
        self.img.setFixedHeight(800)

        self.run = QPushButton("Run")
        self.v.addWidget(self.run)
        self.v.addWidget(self.img)

        self.fileA = InputPicker("A", self.img)
        self.fileB = InputPicker("B", self.img)
        self.fileC = OutputPicker("C", self.img)

        self.h.addWidget(self.fileA)
        self.h.addWidget(self.fileB)
        self.h.addWidget(self.fileC)
        self.h.addLayout(self.v)

        self.setLayout(self.h)

        self.run.clicked.connect(self.run_alorithm)

    def run_alorithm(self):
        self.diff = DiffMerge(self.fileA.folder, self.fileB.folder, self.fileC.folder, 15)
        self.diff.load()
        self.diff.diff_and_merge()
        self.diff.create_merge()

        src = [x[0] for x in self.diff.merge_paths]
        self.fileC.update_files(src)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(1000, 600)
    widget.show()

    sys.exit(app.exec_())
