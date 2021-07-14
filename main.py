import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QAction, QDesktopWidget

from components.device_list import DeviceList
from components.device_map import DeviceMap
from components.player import Player
from components.properties_list import PropertiesList
from models.device import  Device


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        devices = Device.sample()
        #
        self.device_list = DeviceList(devices)
        # self.player = Player(devices[0].device_url)
        # self.properties_list = PropertiesList(devices[0].properties_list)
        # self.device_list.trigger_change_device_for_player.connect(self.player.change_device)
        # self.device_list.trigger_change_device_for_properties.connect(self.properties_list.update_list)
        #
        # widget = QWidget(self)
        # self.setCentralWidget(widget)
        #
        # layout = QHBoxLayout()
        # layout.addWidget(self.device_list)
        # layout.addWidget(self.player)
        # layout.addWidget(self.properties_list)
        # widget.setLayout(layout)
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
        self.device_map = DeviceMap(devices)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(self.device_list)
        layout.addWidget(self.device_map)
        widget.setLayout(layout)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = Terminal()
    terminal.resize(1280, 720)
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
