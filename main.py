from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import(
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QListWidget, QFileDialog
)

import os

app = QApplication([])
win = QWidget()

win.resize(700, 500)
win.setWindowTitle("Easy Editor")

btn_directory = QPushButton("Папка")
list_photos = QListWidget()
v1 = QVBoxLayout()
v1.addWidget(btn_directory)
v1.addWidget(list_photos)

btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_miror = QPushButton("Відзеркалити")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

h1 = QHBoxLayout()
h1.addWidget(btn_left)
h1.addWidget(btn_right)
h1.addWidget(btn_miror)
h1.addWidget(btn_sharp)
h1.addWidget(btn_bw)

picture = QLabel("Картинка")

v2 = QVBoxLayout()
v2.addWidget(picture)
v2.addLayout(h1)

h_main = QHBoxLayout()
h_main.addLayout(v1, 20)
h_main.addLayout(v2, 80)

win.setLayout(h_main)

workdir = ''

def filter(files, ext):
    photos = []
    for file in files:
        for e in ext:
            if file.endswith(e):
                photos.append(file)
    return photos

def open_folder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def get_files():
    open_folder()
    files = os.listdir(workdir)
    ext = ['.png', '.jpg', '.jpeg']
    list_photos.addItems(filter(files, ext))

btn_directory.clicked.connect(get_files)





















win.show()
app.exec_()
