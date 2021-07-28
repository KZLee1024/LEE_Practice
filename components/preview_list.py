from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QScrollArea
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from models.device import Device


class PreviewList(QScrollArea):
    player_list = []

    def __init__(self, devices):
        super().__init__()
        self.devices = devices

        self.setMinimumWidth(550)
        self.setMaximumWidth(550)
        self.scroll_container = QWidget()

        layout = QVBoxLayout()
        for device in self.devices:
            layout.addWidget(self.generate_single_preview(device))
        print(len(self.player_list))
        print(self.player_list[0].PlayingState)
        self.scroll_container.setLayout(layout)

        self.setWidget(self.scroll_container)

    def generate_single_preview(self, device: Device) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        tiny_player_container = QVideoWidget()
        tiny_player_container.setMinimumWidth(480)
        tiny_player_container.setMinimumHeight(320)
        tiny_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        tiny_player.setMedia(QMediaContent(QUrl(device.stream_url)))
        tiny_player.setVolume(0)
        tiny_player.setVideoOutput(tiny_player_container)
        tiny_player.play()

        self.player_list.append(tiny_player)

        label = QLabel(device.title())

        layout.addWidget(tiny_player_container)
        # layout.addWidget(label)

        widget.setLayout(layout)
        return widget
