import threading

from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# from components.device_list_item_widget import DeviceListItemWidget
import global_pars
from utlis.player import Player
from components.properties_list import PropertiesList
from models.device import Device, DeviceType
from components.device_details import DeviceDetails

SIGNAL_PARAMETERS = {'DEVICE_ID': 1}


class DeviceList(QTableWidget):
    trigger_change_device_for_player = pyqtSignal(str)
    trigger_change_device_for_properties = pyqtSignal(dict)
    trigger_change_device_for_map = pyqtSignal(int)
    trigger_change_device_for_previews = pyqtSignal(int)

    trigger_switch_container_for_detail = pyqtSignal(int, QLabel)
    trigger_close_device_detail = pyqtSignal(int)
    # TODO:
    trigger_update_parameters_for_device_detail = pyqtSignal(int, dict)

    pars_label = global_pars.PARAMETER_KEYS

    def __init__(self, device_list):
        self.devices = device_list
        # self.properties = list(self.devices[0].properties.keys())
        self.properties = [{} for _ in range(len(self.devices))]
        for index in range(len(self.devices)):
            for label in self.pars_label:
                self.properties[index][label] = []

        print(self.properties)

        super().__init__(len(self.devices), len(self.pars_label) + 2)

        self.setMinimumHeight(200)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setStyleSheet(
            "color:white;font-size:15px;font-family:song;background-color:#2C3E50;selection-background-color: #84AF9B")
        self.setHorizontalHeaderLabels([' '] + self.pars_label)
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

            self.setHorizontalHeaderItem(len(self.pars_label) + 1, QTableWidgetItem("详情显示"))
            self.btn_list[row].setDown(False)
            self.btn_list[row].setStyleSheet("QPushButton{margin:5px};")
            self.btn_list[row].setStyleSheet("color:black;font-size:25px;font-weight:bold;font-family:Roman times;")
            self.btn_list[row].setStyleSheet("background-color:darkcyan")
            self.setCellWidget(row, len(self.pars_label) + 1, self.btn_list[row])

            col = 1
            for property in self.pars_label:
                # The device instance holds only the initial value of their properties
                # And that's exactly what is needed here
                if self.devices[row].properties[property] is not None:
                    QTableWidgetItem(self.devices[row].properties[self.pars_label[col - 1]]).setForeground(
                        QBrush(QColor(255, 0, 0)))
                    self.setItem(row, col, QTableWidgetItem(self.devices[row].properties[self.pars_label[col - 1]]))
                else:
                    QTableWidgetItem(' - ').setForeground(QBrush(QColor(255, 0, 0)))
                    self.setItem(row, col, QTableWidgetItem(' - '))
                col += 1

        if len(self.devices) > 0:
            self.selectRow(0)

        self.currentCellChanged.connect(self.change_device)
        self.cellDoubleClicked.connect(self.play_specific_device)

        for row in range(len(self.devices)):
            # self.btn_list[row].clicked.connect(lambda _, row=row: self.trigger_play.emit(self.devices[row]))
            self.btn_list[row].clicked.connect(lambda _, row=row: self.play_specific_device(row))

    def change_device(self, current_row):
        self.trigger_change_device_for_map.emit(current_row)

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play_specific_device(self, device_index):
        print('generating full-screen player')
        self.deviceDetail = DeviceDetails(device_index, self.devices[device_index], self.properties[device_index])
        # ready for window close
        self.deviceDetail.trigger_close_device_detail.connect(self.close_device_detail)

        self.trigger_switch_container_for_detail.emit(device_index, self.deviceDetail.get_player_container())
        self.trigger_update_parameters_for_device_detail.connect(self.deviceDetail.push_data_handler)

        self.deviceDetail.setAttribute(Qt.WA_DeleteOnClose)
        # self.deviceDetail.resize(2100, 1600)
        self.deviceDetail.show()

    def close_device_detail(self, device_index):
        self.trigger_close_device_detail.emit(device_index)

    def update_parameter_handler(self, device_index, pars: dict):
        print(device_index, pars)

        oldValue, newValue = -1, -1
        newLabel = '-'

        full_screen_pars = {}

        for key, value in pars.items():
            col = global_pars.PARAMETER_KEYS.index(key) + 1
            if col <= 0:
                continue

            if key == 'Loss-Rate':
                oldLabel = self.item(device_index, col).text()
                if oldLabel != '-':
                    oldValue = float(oldLabel[:-1])
                newValue = round(value, 2)
                newLabel = str(newValue) + '%'
                self.properties[device_index]['Loss-Rate'].append(newValue)
                if len(self.properties[device_index]['Loss-Rate']) > 5:
                    self.properties[device_index]['Loss-Rate'].pop(0)
                full_screen_pars['Loss-Rate'] = newValue
            elif key == 'Latency':
                oldLabel = self.item(device_index, col).text()
                if oldLabel != '-':
                    oldValue = float(oldLabel[:-2])
                newValue = round(value, 2)
                newLabel = str(newValue) + 'ms'
                self.properties[device_index]['Latency'].append(newValue)
                if len(self.properties[device_index]['Latency']) > 5:
                    self.properties[device_index]['Latency'].pop(0)
                full_screen_pars['Latency'] = newValue
            elif key == 'Channel':
                oldLabel = self.item(device_index, col).text()
                if oldLabel != '-':
                    oldValue = int(oldLabel[:-3])
                newValue = int(value)
                newLabel = str(newValue) + 'MHz'
                self.properties[device_index]['Channel'].append(newValue)
                if len(self.properties[device_index]['Channel']) > 5:
                    self.properties[device_index]['Channel'].pop(0)
                full_screen_pars['Channel'] = newValue
            elif key == 'Power':
                oldLabel = self.item(device_index, col).text()
                if oldLabel != '-':
                    oldValue = int(oldLabel[:-2])
                newValue = int(value)
                newLabel = str(newValue) + 'mW'
                self.properties[device_index]['Power'].append(newValue)
                if len(self.properties[device_index]['Power']) > 5:
                    self.properties[device_index]['Power'].pop(0)
                full_screen_pars['Power'] = newValue

            self.item(device_index, col).setText(newLabel)
            if newValue > oldValue:
                color = Qt.red
            elif newValue < oldValue:
                color = Qt.blue
            else:
                color = Qt.black
            self.item(device_index, col).setForeground(color)

        self.trigger_update_parameters_for_device_detail.emit(device_index, full_screen_pars)
