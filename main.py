import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget

from Components.device_list import DeviceList
from Components.stream_player import Player


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("qiyuan-terminal")

        deviceList = DeviceList()
        player = Player()

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(deviceList)
        layout.addWidget(player)
        widget.setLayout(layout)

        self.statusBar()
        openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open movie')
        openFileAction.triggered.connect(player.open_file)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu(' &File')
        fileMenu.addAction(openFileAction)

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
