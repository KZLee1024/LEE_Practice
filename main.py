import sys

from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QStyle, QWidget, QVBoxLayout, QFileDialog, \
    QInputDialog, QHBoxLayout, QGridLayout, QAction, QDesktopWidget


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("qiyuan-terminal")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.buttonOpen = QPushButton(QIcon("./assets/icons/live_tv.svg"), "Open", self)
        self.buttonOpen.setStatusTip("Open Live Stream")
        self.buttonOpen.resize(self.buttonOpen.sizeHint())
        self.buttonOpen.clicked.connect(self.open_stream)

        self.buttonPlay = QPushButton(QIcon("./assets/icons/play.svg"), "Play", self)
        self.buttonPlay.setStatusTip("Play / Pause")
        self.buttonPlay.resize(self.buttonPlay.sizeHint())
        self.buttonPlay.clicked.connect(self.play)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(self.buttonOpen)
        hBox.addWidget(self.buttonPlay)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(hBox)

        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)

        self.statusBar()
        openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open movie')
        openFileAction.triggered.connect(self.open_file)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu(' &File')
        fileMenu.addAction(openFileAction)

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
            self.buttonPlay.setIcon(QIcon("./assets/icons/pause.svg"))
            self.buttonPlay.setText("Pause")
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.buttonPlay.setIcon(QIcon("./assets/icons/play.svg"))
            self.buttonPlay.setText("Play")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoPlayer = VideoPlayer()
    videoPlayer.resize(1280, 720)
    videoPlayer.center()
    videoPlayer.show()
    sys.exit(app.exec_())

