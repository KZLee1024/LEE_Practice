from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout

from components.player import Player
from components.properties_list import PropertiesList

SIGNAL_PARAMETERS = {'DEVICE_ID': 1}


class DeviceList(QListWidget):
    trigger_change_device_for_player = pyqtSignal(str)
    trigger_change_device_for_properties = pyqtSignal(dict)
    trigger_change_device_for_map = pyqtSignal(int)

    def __init__(self, device_list):
        super().__init__()

        self.devices = device_list

        self.setSpacing(10)
        self.setMaximumWidth(200)
        for device in device_list:
            item = QListWidgetItem(device.title())
            # Add customized parameter 'deviceId' for index of '1'
            item.setData(SIGNAL_PARAMETERS['DEVICE_ID'], device.device_id)
            self.addItem(item)
            if device.device_id == 0:
                print('first device selected, the url is: ' + device.stream_url)
                self.setCurrentItem(item)

        self.currentItemChanged.connect(self.change_device)
        self.itemDoubleClicked.connect(self.play)

    def change_device(self, current):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(self.currentRow())

    def play(self, item):
        player = Player(self.devices[self.currentRow()].stream_url)
        properties = PropertiesList(self.devices[self.currentRow()].properties)

        window_player = QMainWindow(self)

        widget = QWidget(self)
        widget.setGeometry(0,0, 500, 300)
        window_player.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(player)
        layout.addWidget(properties)
        widget.setLayout(layout)

        window_player.setAttribute(Qt.WA_DeleteOnClose)
        window_player.resize(800, 500)
        window_player.show()
