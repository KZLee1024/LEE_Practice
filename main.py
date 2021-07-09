import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget

from Components.device_list import DeviceList
from Components.player import Player
from Components.properties_list import PropertiesList


class Device:
    deviceId: int = -1
    deviceTitle = ""
    deviceUrl = ""

    def __init__(self, id, title, url, properties):
        self.deviceId = id
        self.deviceTitle = title
        self.deviceUrl = url
        self.propertiesList = properties


devices = [Device(0, "CCTV-1", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8",
                  {"Loss Rate": "30%", "Latency": "50ms", "Channel": "2421MHz", "Power": "100mW"}),
           Device(1, "CCTV-3", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8",
                  {"Loss Rate": "27%", "Latency": "30ms", "Channel": "2421MHz", "Power": "100mW"}),
           Device(2, "CCTV-6", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8",
                  {"Loss Rate": "5%", "Latency": "5ms", "Channel": "2421MHz", "Power": "100mW"}),
           Device(3, "dash",
                  "https://dash.akamaized.net/dash264/TestCasesIOP33/adapatationSetSwitching/5/manifest.mpd",
                  {"Loss Rate": "100%", "Latency": "-", "Channel": "2421MHz", "Power": "100mW"})]


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.deviceList = DeviceList(devices)
        self.player = Player(devices[0].deviceUrl)
        self.properties_list = PropertiesList(devices[0].propertiesList)
        self.deviceList.trigger_change_device_for_player.connect(self.player.change_device)
        self.deviceList.trigger_change_device_for_properties.connect(self.properties_list.update_list)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(self.deviceList)
        layout.addWidget(self.player)
        layout.addWidget(self.properties_list)
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
