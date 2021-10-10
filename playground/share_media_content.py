import sys
import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton, \
    QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from models.device import Device
from utlis.player import Player

devices = Device.sample()

class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()

        self.player_container_0 = QLabel()
        self.player_container_1 = QLabel()

        self.player = Player(self.player_container_0, device=devices[0])

        threading.Thread(target=self.player.display, daemon=True).start()

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
        self.player.switch_container()

    def switch_to_1(self):
        self.player.switch_container(self.player_container_1)

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
