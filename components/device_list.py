from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# from components.device_list_item_widget import DeviceListItemWidget
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

        super().__init__(len(self.devices), len(self.properties)+2)

        self.setMinimumHeight(200)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet("color:white;font-size:15px;font-family:song;background-color:#2C3E50;selection-background-color: #84AF9B")
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
        self.btn_list = [QPushButton("选择") for i in range(len(self.devices))]

        for row in range(len(self.devices)):
            self.setItem(row, 0, QTableWidgetItem(self.devices[row].title()))

            self.setHorizontalHeaderItem(len(self.properties) + 1, QTableWidgetItem("全屏显示"))
            self.btn_list[row].setDown(False)
            self.btn_list[row].setStyleSheet("QPushButton{margin:5px};")
            self.btn_list[row].setStyleSheet("color:black;font-size:25px;font-weight:bold;font-family:Roman times;")
            self.btn_list[row].setStyleSheet("background-color:darkcyan")
            self.setCellWidget(row, len(self.properties) + 1, self.btn_list[row])

            col = 1
            for property in self.properties:
                if self.devices[row].properties[property] is not None:
                    QTableWidgetItem(self.devices[row].properties[self.properties[col - 1]]).setForeground(QBrush(QColor(255, 0, 0)))
                    self.setItem(row, col, QTableWidgetItem(self.devices[row].properties[self.properties[col - 1]]))

                else:
                    QTableWidgetItem(' - ').setForeground(QBrush(QColor(255, 0, 0)))
                    self.setItem(row, col, QTableWidgetItem(' - '))
                col += 1

        if len(self.devices) > 0:
            self.selectRow(0)

        self.currentCellChanged.connect(self.change_device)
        self.cellDoubleClicked.connect(self.play_specific_device)

        for row in range(len(self.devices)):
            self.btn_list[row].clicked.connect(lambda _, row = row: self.trigger_play.emit(self.devices[row]))

    def change_device(self, current_row):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(current_row)
        # self.trigger_play.emit(self.devices[current_row])
    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play_specific_device(self, row):
        self.trigger_play.emit(self.devices[row])
