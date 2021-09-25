import sys
import threading

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget, QVBoxLayout, \
    QFileDialog, QLabel

from components.device_list import DeviceList
from components.device_map import DeviceMap
from components.preview_list import PreviewList

from models.device import Device, DeviceType
from utlis.player import Player
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

        # self.statusBar()
        self.menu_bar = self.menuBar()

        self.connect_component_signals()
        self.init_menu_actions()
        self.full_screen()

        self.setWindowTitle("Terminal")

        widget = QWidget(self)
        widget.setAutoFillBackground(True)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        r_layout = QVBoxLayout()

        r_layout.addWidget(self.device_list)
        r_layout.addWidget(self.device_map)
        layout.addWidget(self.preview_list)
        layout.addLayout(r_layout)

        widget.setLayout(layout)
        palette = QPalette()
        palette.setColor(widget.backgroundRole(), QColor(0, 0, 0, 150))
        widget.setPalette(palette)

    def showMaximized(self):
        '''最大化'''
        # 得到桌面控件
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.availableGeometry()
        # 设置窗口尺寸
        self.setGeometry(rect)
        # 设置窗口显示
        self.show()

    def connect_component_signals(self):
        self.device_list.trigger_change_device_for_map.connect(self.device_map.change_device_handler)
        self.device_list.trigger_change_device_for_map.connect(self.preview_list.change_device_handler)
        self.device_list.trigger_play.connect(self.play_specific_stream_handler)

        self.client.trigger_move_device.connect(self.device_map.move_device_handler)
        self.client.trigger_update_parameter.connect(self.device_list.update_parameter_handler)

    def init_menu_actions(self):
        openFileAction = QAction(QIcon("./assets/icons/folder.svg"), "&Open", self)
        openFileAction.setShortcut('Ctrl+O')
        # openFileAction.setStatusTip('Open movie')
        openFileAction.triggered.connect(self.play_specific_local_video_handler)

        file_menu = self.menu_bar.addMenu(' &File')
        file_menu.addAction(openFileAction)

    def full_screen(self):
        # self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setStyleSheet('''background-color:blue; ''')
        self.showMaximized()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def play_specific_local_video_handler(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Movie", QDir.homePath())
        print(file_name)
        container = self.show_player()
        threading.Thread(target=Player(container=container, local_file=file_name).display).start()

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play_specific_stream_handler(self, device):
        if device.device_type != DeviceType.undefined:
            container = self.show_player()
            threading.Thread(target=Player(container=container, device=device).display, daemon=True).start()

    def show_player(self) -> QLabel:
        window_player = QMainWindow(self)

        widget = QWidget(self)
        window_player.setCentralWidget(widget)

        container = QLabel()
        container.setMinimumWidth(2000)
        container.setMinimumHeight(1500)
        container.setText("")
        container.setObjectName("FullScreenVideo")

        layout = QHBoxLayout()
        layout.addWidget(container)
        # layout.addWidget(properties)
        widget.setLayout(layout)

        window_player.setAttribute(Qt.WA_DeleteOnClose)
        window_player.resize(2100, 1600)
        window_player.show()

        return container


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = Terminal()
    # terminal.resize(1280, 720)
    terminal.center()
    # terminal.show()
    terminal.showFullScreen()
    sys.exit(app.exec_())
