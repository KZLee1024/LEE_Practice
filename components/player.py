from global_pars import BASE_DIR

from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QFileDialog, QInputDialog, QHBoxLayout

from PyQt5.QtWidgets import QWidget


class Player(QWidget):
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
