import threading

import cv2
import time
from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtGui import QPalette, QImage, QPixmap
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QScrollArea, QGridLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from models.device import Device


class Preview:
    FPS = -1
    FPS_MS = -1

    def __init__(self, device, container):
        self.device = device
        self.container = container

    def display(self):
        print("# DISPLAY_VIDEO --- loading")
        cap = cv2.VideoCapture(self.device.stream_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

        print(self.container)

        FPS = 1 / int(cap.get(cv2.CAP_PROP_FPS))
        FPS_MS = int(FPS * 1000)

        print("# DISPLAY_VIDEO --- displaying")

        while cap.isOpened():
            success, frame = cap.read()
            time.sleep(FPS)
            if success:
                img = frame.copy()
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                # Keep width-height ratio and Resize
                container_width, container_height = 360, 320
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


class PreviewList(QScrollArea):
    previews = []
    selected_preview_index = -1

    def __init__(self, devices):
        super().__init__()
        self.devices = devices

        self.setMinimumWidth(795)
        self.setMaximumWidth(795)
        self.scroll_container = QWidget()

        layout = QGridLayout()
        layout.setSpacing(0)
        row, col = 0, 0

        for index in range(len(self.devices)):
            new_preview = QLabel()
            new_preview.setMinimumWidth(360)
            new_preview.setMinimumHeight(320)
            new_preview.setText("")
            new_preview.setObjectName("video-" + str(index))

            label = QLabel(self.devices[index].title())
            h_box = QHBoxLayout()
            h_box.addStretch(1)
            h_box.addWidget(label)
            h_box.addStretch(1)

            layout_container_preview = QVBoxLayout()
            layout_container_preview.addWidget(new_preview)
            layout_container_preview.addLayout(h_box)

            widget = QWidget()
            widget.setLayout(layout_container_preview)
            widget.setAutoFillBackground(True)

            layout.addWidget(widget, row, col)
            self.previews.append(widget)

            threading.Thread(target=Preview(self.devices[index], new_preview).display).start()

            if index % 2 == 0:
                col = 1
            else:
                col = 0
                row += 1

        if len(self.previews) > 0:
            self.change_device_handler(0)

        print(len(self.previews))
        print(self.previews[0])
        self.scroll_container.setLayout(layout)

        self.setWidget(self.scroll_container)
        self.scroll_container.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(self.scroll_container.backgroundRole(), Qt.transparent)
        self.scroll_container.setPalette(palette)

    def change_device_handler(self, new_index):
        if self.selected_preview_index != -1:
            palette = self.previews[self.selected_preview_index].palette()
            palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.transparent)
            self.previews[self.selected_preview_index].setPalette(palette)

        self.selected_preview_index = new_index

        palette = self.previews[self.selected_preview_index].palette()
        palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.red)
        self.previews[self.selected_preview_index].setPalette(palette)
