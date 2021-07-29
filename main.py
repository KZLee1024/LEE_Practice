import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget, QVBoxLayout

from components.device_list import DeviceList
from components.device_map import DeviceMap
from components.player import Player
from components.preview_list import PreviewList
from components.properties_list import PropertiesList
from models.device import Device


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        devices = Device.sample()
        #
        self.device_list = DeviceList(devices)
        self.device_map = DeviceMap(devices)
        self.preview_list = PreviewList(devices)
        # self.player = Player(devices[0].stream_url)
        # self.properties_list = PropertiesList(devices[0].properties_list)
        # self.device_list.trigger_change_device_for_player.connect(self.player.change_device)
        # self.device_list.trigger_change_device_for_properties.connect(self.properties_list.update_list)
        self.device_list.trigger_change_device_for_map.connect(self.device_map.change_device_handler)
        self.device_list.trigger_change_device_for_map.connect(self.preview_list.change_device_handler)
        #
        # widget = QWidget(self)
        # self.setCentralWidget(widget)
        #
        # r_layout = QHBoxLayout()
        # r_layout.addWidget(self.device_list)
        # r_layout.addWidget(self.player)
        # r_layout.addWidget(self.properties_list)
        # widget.setLayout(r_layout)
        #
        # self.statusBar()
        # openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        # openFileAction.setShortcut('Ctrl+O')
        # openFileAction.setStatusTip('Open movie')
        # openFileAction.triggered.connect(self.player.open_file)
        #
        # menu_bar = self.menuBar()
        # file_menu = menu_bar.addMenu(' &File')
        # file_menu.addAction(openFileAction)

        self.setWindowTitle("qiyuan-terminal")

        # Try

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        r_layout = QVBoxLayout()

        r_layout.addWidget(self.device_list)
        r_layout.addWidget(self.device_map)
        layout.addWidget(self.preview_list)
        layout.addLayout(r_layout)

        widget.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = Terminal()
    # terminal.resize(1280, 720)
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
