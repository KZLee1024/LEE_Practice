from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QScrollArea
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from models.device import Device


class PreviewList(QScrollArea):
    previews = []
    selected_preview_index = -1

    def __init__(self, devices):
        super().__init__()
        self.devices = devices

        self.setMinimumWidth(550)
        self.setMaximumWidth(550)
        self.scroll_container = QWidget()

        layout = QVBoxLayout()
        layout.setSpacing(10)
        for device in self.devices:
            new_preview = self.Preview(device)
            layout.addWidget(new_preview)
            self.previews.append(new_preview)

        if len(self.previews) > 0:
            self.change_device_handler(0)

        print(len(self.previews))
        print(self.previews[0])
        print(self.previews[0].tiny_player.PlayingState)
        self.scroll_container.setLayout(layout)

        self.setWidget(self.scroll_container)

    def change_device_handler(self, new_index):
        if self.selected_preview_index != -1:
            palette = self.previews[self.selected_preview_index].palette()
            palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.transparent)
            self.previews[self.selected_preview_index].setPalette(palette)

        self.selected_preview_index = new_index

        palette = self.previews[self.selected_preview_index].palette()
        palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.green)
        self.previews[self.selected_preview_index].setPalette(palette)

    class Preview(QWidget):
        def __init__(self, device):
            super().__init__()

            self.layout = QVBoxLayout()

            self.tiny_player_container = QVideoWidget()
            self.tiny_player_container.setMinimumWidth(480)
            self.tiny_player_container.setMinimumHeight(320)
            self.tiny_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            self.tiny_player.setMedia(QMediaContent(QUrl(device.stream_url)))
            self.tiny_player.setVolume(0)
            self.tiny_player.setVideoOutput(self.tiny_player_container)
            self.tiny_player.play()

            label = QLabel(device.title())
            b_layout = QHBoxLayout()
            b_layout.addStretch(1)
            b_layout.addWidget(label)
            b_layout.addStretch(1)

            self.layout.addWidget(self.tiny_player_container)
            self.layout.addLayout(b_layout)

            self.setLayout(self.layout)
            self.setAutoFillBackground(True)


