from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QFileDialog, QInputDialog, QHBoxLayout

from PyQt5.QtWidgets import QWidget


class Player(QWidget):
    def __init__(self):
        super().__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.buttonOpen = QPushButton(QIcon("../assets/icons/live_tv.svg"), "Open", self)
        self.buttonOpen.setStatusTip("Open Live Stream")
        self.buttonOpen.resize(self.buttonOpen.sizeHint())
        self.buttonOpen.clicked.connect(self.open_stream)

        self.buttonPlay = QPushButton(QIcon("../assets/icons/play.svg"), "Play", self)
        self.buttonPlay.setStatusTip("Play / Pause")
        self.buttonPlay.resize(self.buttonPlay.sizeHint())
        self.buttonPlay.clicked.connect(self.play)

        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(self.buttonOpen)
        hBox.addWidget(self.buttonPlay)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(hBox)

        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if fileName != ' ':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mediaPlayer.play()
            self.update_button_display()

    def open_stream(self):
        url, ok = QInputDialog().getText(self, 'Stream Url', 'Enter the url of stream live')
        if ok:
            self.mediaPlayer.setMedia(QMediaContent(QUrl(url)))
            self.mediaPlayer.play()
            self.update_button_display()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.update_button_display()
        else:
            self.mediaPlayer.play()
            self.update_button_display()

    def update_button_display(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.buttonPlay.setIcon(QIcon("../assets/icons/pause.svg"))
            self.buttonPlay.setText("Pause")
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.buttonPlay.setIcon(QIcon("../assets/icons/play.svg"))
            self.buttonPlay.setText("Play")
