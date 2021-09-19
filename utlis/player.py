import time

import cv2

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

    def __init__(self, device, container):
        self.device = device
        self.container:QLabel = container

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


class Player0(QWidget):
    def __init__(self):
        super().__init__()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()

        self.button_play = QPushButton(QIcon(BASE_DIR + "/assets/icons/play.svg"), "Play", self)
        self.button_play.setStatusTip("Play / Pause")
        self.button_play.resize(self.button_play.sizeHint())
        self.button_play.clicked.connect(self.play)

        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(self.button_play)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(h_box)

        self.setLayout(layout)
        self.media_player.setVideoOutput(video_widget)

    def open_file(self, file_name):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
        self.media_player.play()
        self.update_button_display()

    def open_stream(self, source_url):
        # url, ok = QInputDialog().getText(self, 'Stream Url', 'Enter the url of stream live')
        self.media_player.setMedia(QMediaContent(QUrl(source_url)))
        self.media_player.play()
        self.update_button_display()

    def play(self):
        print(self.media_player.state())
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.update_button_display()
        else:
            self.media_player.play()
            self.update_button_display()

    def update_button_display(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.button_play.setIcon(QIcon(BASE_DIR + "/assets/icons/pause.svg"))
            self.button_play.setText("Pause")
        elif self.media_player.state() == QMediaPlayer.PausedState:
            self.button_play.setIcon(QIcon(BASE_DIR + "/assets/icons/play.svg"))
            self.button_play.setText("Play")

    def change_device(self, url):
        print("player has received signal, and url is: ", url)
        if len(self.media_player.currentMedia().resources()) != 0:
            print(self.media_player.currentMedia().resources()[0].url())
        self.media_player.setMedia(QMediaContent(QUrl(url)))
        print(self.media_player.currentMedia().resources()[0].url())
        print(self.media_player.state())
        self.media_player.play()
        print(self.media_player.state())
        self.update_button_display()
