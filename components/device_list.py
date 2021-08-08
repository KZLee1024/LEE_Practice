from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# from components.device_list_item_widget import DeviceListItemWidget
from components.player import Player
from components.properties_list import PropertiesList
from models.device import Device

SIGNAL_PARAMETERS = {'DEVICE_ID': 1}


class DeviceList(QTableWidget):
    trigger_change_device_for_player = pyqtSignal(str)
    trigger_change_device_for_properties = pyqtSignal(dict)
    trigger_change_device_for_map = pyqtSignal(int)
    trigger_change_device_for_previews = pyqtSignal(int)

    trigger_play = pyqtSignal(Device)

    def __init__(self, device_list):
        self.devices = device_list
        self.properties = list(self.devices[0].properties.keys())
        print(self.properties)

        super().__init__(len(self.devices), len(self.properties))

        self.setMinimumHeight(200)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setHorizontalHeaderLabels([' '] + self.properties)
        self.setVerticalHeaderLabels(map(str, range(1, len(self.devices))))

        # cannot be edited
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Select single row once
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # Select as the whole row
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Auto resize width and height
        # QTableWidget.resizeColumnToContents(self)
        # QTableWidget.resizeRowToContents(self)

        for row in range(len(self.devices)):
            self.setItem(row, 0, QTableWidgetItem(self.devices[row].title()))
            col = 1
            for property in self.properties:
                if self.devices[row].properties[property] is not None:
                    self.setItem(row, col, QTableWidgetItem(self.devices[row].properties[self.properties[col - 1]]))
                else:
                    self.setItem(row, col, QTableWidgetItem(' - '))
                col += 1
        if len(self.devices) > 0:
            self.selectRow(0)

        self.currentCellChanged.connect(self.change_device)
        self.cellDoubleClicked.connect(self.play_specific_device)

    def change_device(self, current_row):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(current_row)

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play_specific_device(self, row, _):
        self.trigger_play.emit(self.devices[row])
