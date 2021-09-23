import threading
import time

import cv2
import sip

from global_pars import BASE_DIR

from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QFileDialog, QInputDialog, QHBoxLayout, QLabel

from PyQt5.QtWidgets import QWidget


class Player:
    FPS = -1
    FPS_MS = -1

    def __init__(self, container, device=None, local_file=None):
        self.container: QLabel = container
        self.device = device
        self.local_file = local_file

    def display(self):
        print("# DISPLAY_VIDEO --- loading")
        if self.device is not None:
            cap = cv2.VideoCapture(self.device.stream_url)
        else:
            cap = cv2.VideoCapture(self.local_file)

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

        print(self.container)

        FPS = 1 / int(cap.get(cv2.CAP_PROP_FPS))
        FPS_MS = int(FPS * 1000)

        print("# DISPLAY_VIDEO --- displaying")

        while cap.isOpened():
            print(threading.active_count())
            # print("playing...")
            success, frame = cap.read()
            time.sleep(FPS)
            if success:
                img = frame.copy()
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                if sip.isdeleted(self.container):
                    break

                # Keep width-height ratio while resizing
                container_width, container_height = self.container.size().width(), self.container.size().height()
                width, height = img.shape[1], img.shape[0]
                if width / height >= container_width / container_height:
                    img = cv2.resize(img, (container_width, int(height * container_width / width)))
                else:
                    img = cv2.resize(img, (int(width * container_height / height), container_height))
                img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)

                self.container.setPixmap(QPixmap.fromImage(img))
            else:
                self.container.clear()
                break

        try:
            cap.release()
        except:
            print("# ERROR @ Resource Release")