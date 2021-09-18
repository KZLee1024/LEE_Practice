import sys
import time

import cv2
import threading

from PyQt5.QtCore import QUrl, QRect
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton, \
    QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QImage, QPixmap

test_url = "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8"


class Player:
    def __init__(self, url, container):
        self.url = url
        self.container = container

    def display(self):
        print("# DISPLAY_VIDEO --- loading")
        cap = cv2.VideoCapture(self.url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

        print(self.container)

        FPS = 1 / int(cap.get(cv2.CAP_PROP_FPS))
        FPS_MS = int(FPS * 100)

        print("# DISPLAY_VIDEO --- displaying")

        while cap.isOpened():
            success, frame = cap.read()
            time.sleep(FPS)
            if success:
                img = frame.copy()
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                # img = cv2.resize(img, (1080, 540))
                img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                self.container.setPixmap(QPixmap.fromImage(img))
                cv2.waitKey(1)
            else:
                self.container.clear()
                break

        try:
            cap.release()
        except:
            print("# ERROR @ Resource Release")


class Terminal(QMainWindow):
    # players = []

    def __init__(self):
        super().__init__()

        self.video_thread = None
        self.cap = None

        self.stop_event = threading.Event()
        self.stop_event.clear()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.video_container_0 = QLabel()
        self.video_container_0.setGeometry(QRect(270, 60, 1031, 541))
        self.video_container_0.setAutoFillBackground(True)
        self.video_container_0.setStyleSheet("border-width: 1px;\n"
                                             "background-color: rgb(255, 255, 255);\n"
                                             "border-style: solid;\n"
                                             "border-color: rgb(0, 0, 0)")
        self.video_container_0.setText("")
        self.video_container_0.setObjectName("video_plate_0")

        self.video_container_1 = QLabel()
        self.video_container_1.setGeometry(QRect(270, 60, 1031, 541))
        self.video_container_1.setAutoFillBackground(True)
        self.video_container_1.setStyleSheet("border-width: 1px;\n"
                                             "background-color: rgb(255, 255, 255);\n"
                                             "border-style: solid;\n"
                                             "border-color: rgb(0, 0, 0)")
        self.video_container_1.setText("")
        self.video_container_1.setObjectName("video_plate_1")

        print(self.video_container_0)
        print(self.video_container_1)

        # self.players.append(self.video_container_0)
        # self.players.append(self.video_container_1)

        self.button_load = QPushButton("Load Video")
        self.button_load.clicked.connect(self.load_video)

        layout = QVBoxLayout()

        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.video_container_0)
        upper_layout.addWidget(self.video_container_1)

        layout.addLayout(upper_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.button_load)

        layout.addLayout(bottom_layout)
        widget.setLayout(layout)

        self.launch_player()

    def launch_player(self):
        threading.Thread(target=Player(test_url, self.video_container_0).display).start()
        threading.Thread(target=Player(test_url, self.video_container_1).display).start()

    def load_video(self):
        if self.video_thread is None:
            self.video_thread = threading.Thread(target=self.display_video, daemon=True)
            self.video_thread.start()

    def close_video(self):
        self.stop_event.set()

    def display_video(self):
        print("# DISPLAY_VIDEO --- loading")
        self.cap = cv2.VideoCapture(test_url)
        print(self.cap)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

        self.FPS = 1 / int(self.cap.get(cv2.CAP_PROP_FPS))
        self.FPS_MS = int(self.FPS * 1000)

        print("# DISPLAY_VIDEO --- displaying")
        while self.cap.isOpened():
            print("cap alive")
            ret, frame = self.cap.read()
            time.sleep(self.FPS)
            if ret:
                img = frame.copy()
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                # img = cv2.resize(img, (1080, 540))
                img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                print(img)
                self.video_container_0.setPixmap(QPixmap.fromImage(img))

                if self.stop_event.is_set():
                    self.stop_event.clear()
                    self.play.clear()
                    break
            else:
                self.video_container_0.clear()
                break

        try:
            self.cap.release()
        except:
            print("# ERROR @ Resource Release")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = Terminal()
    terminal.resize(1000, 500)
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
