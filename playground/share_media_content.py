import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()

        self.player_container_0 = QVideoWidget()
        self.player_container_1 = QVideoWidget()
        # player_container_0.setGeometry(0,0,480, 360)

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setMedia(QMediaContent(
            QUrl("rtmp://192.168.0.104:1935/live/test")))
        self.player.setVideoOutput(self.player_container_0)
        self.player.setVolume(5)
        self.player.play()

        self.button_20 = QPushButton("<-")
        self.button_20.setMaximumWidth(100)
        self.button_20.clicked.connect(self.switch_to_0)

        self.button_21 = QPushButton("->")
        self.button_21.setMaximumWidth(100)
        self.button_21.clicked.connect(self.switch_to_1)

        la = QVBoxLayout()
        la.addWidget(self.button_20)
        la.addWidget(self.button_21)
        la.setSpacing(50)

        layout = QHBoxLayout()
        layout.addWidget(self.player_container_0)
        layout.addLayout(la)
        layout.addWidget(self.player_container_1)
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def switch_to_0(self):
        self.player.setVideoOutput(self.player_container_0)

    def switch_to_1(self):
        self.player.setVideoOutput(self.player_container_1)

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
