import sys

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget, QVBoxLayout, QFileDialog

from components.device_list import DeviceList
from components.device_map import DeviceMap
from components.player import Player
from components.preview_list import PreviewList
from components.properties_list import PropertiesList

from models.device import Device, DeviceType
from utlis.udp_client import UDPClient


class Terminal(QMainWindow):
    player = None

    def __init__(self):
        super().__init__()

        devices = Device.sample()

        self.client = UDPClient()

        self.device_list = DeviceList(devices)
        self.device_map = DeviceMap(devices)
        self.preview_list = PreviewList(devices)

        self.statusBar()
        self.menu_bar = self.menuBar()

        self.connect_component_signals()
        self.init_menu_actions()

        self.setWindowTitle("qiyuan-terminal")

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        r_layout = QVBoxLayout()

        r_layout.addWidget(self.device_list)
        r_layout.addWidget(self.device_map)
        layout.addWidget(self.preview_list)
        layout.addLayout(r_layout)

        widget.setLayout(layout)

    def connect_component_signals(self):
        self.device_list.trigger_change_device_for_map.connect(self.device_map.change_device_handler)
        self.device_list.trigger_change_device_for_map.connect(self.preview_list.change_device_handler)
        self.device_list.trigger_play.connect(self.play_specific_stream_handler)
        self.client.trigger_move_device.connect(self.device_map.move_device_handler)

    def init_menu_actions(self):
        openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Open movie')
        openFileAction.triggered.connect(self.play_specific_local_video_handler)

        file_menu = self.menu_bar.addMenu(' &File')
        file_menu.addAction(openFileAction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def play_specific_local_video_handler(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        if file_name != ' ':
            self.player = Player()
            self.player.open_file(file_name)
            self.show_player()

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play_specific_stream_handler(self, device):
        if device.device_type != DeviceType.undefined:
            self.player = Player()
            self.player.open_stream(device.stream_url)
            self.show_player()

    def show_player(self, ):
        window_player = QMainWindow(self)

        widget = QWidget(self)
        window_player.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(self.player)
        # layout.addWidget(properties)
        widget.setLayout(layout)

        window_player.setAttribute(Qt.WA_DeleteOnClose)
        window_player.resize(1080, 720)
        window_player.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = Terminal()
    # terminal.resize(1280, 720)
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
