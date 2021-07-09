import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget

from Components.device_list import DeviceList
from Components.stream_player import Player


class Device:
    deviceId: int = -1
    deviceTitle = ""
    deviceUrl = ""

    def __init__(self, id, title, url):
        self.deviceId = id
        self.deviceTitle = title
        self.deviceUrl = url


devices = [Device(0, "CCTV-1", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8"),
           Device(1, "CCTV-3", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8"),
           Device(2, "CCTV-5", "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8"),
           Device(3, "CCTV-6", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8"),
           Device(4, "dash",
                  "https://dash.akamaized.net/dash264/TestCasesIOP33/adapatationSetSwitching/5/manifest.mpd")]


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.deviceList = DeviceList(devices)
        self.player = Player()
        self.deviceList.trigger_change_device.connect(self.player.change_device)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(self.deviceList)
        layout.addWidget(self.player)
        widget.setLayout(layout)

        self.statusBar()
        openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open movie')
        openFileAction.triggered.connect(self.player.open_file)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu(' &File')
        fileMenu.addAction(openFileAction)

        self.setWindowTitle("qiyuan-terminal")

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
