from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import(
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QListWidget, QFileDialog 
)

from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import Image, ImageFilter
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

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None 
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    #def do_detail(self):
    #    photo = photo.transpose(ImageFilter.DETAIL)
    #    self.saveImage()
    #    image_path = os.path.join(self.dir, self.save_dir, self.filename)
    #    self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()

workimage = ImageProcessor()

def showChosenImage():
    if list_photos.currentRow() >= 0:
        filename = list_photos.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
list_photos.currentRowChanged.connect(showChosenImage)


btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_miror.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
#btn_bw.clicked.connect(workimage.do_detail)

app.exec_()
