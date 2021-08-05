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
        self.cellDoubleClicked.connect(self.play)

    def change_device(self, current_row):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(current_row)

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play(self, row, _):
        player = Player(self.devices[row].stream_url)
        properties = PropertiesList(self.devices[row].properties)

        window_player = QMainWindow(self)

        widget = QWidget(self)
        widget.setGeometry(0, 0, 500, 300)
        window_player.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(player)
        layout.addWidget(properties)
        widget.setLayout(layout)

        window_player.setAttribute(Qt.WA_DeleteOnClose)
        window_player.resize(1000, 700)
        window_player.show()


class DeviceList_0(QListWidget):
    trigger_change_device_for_player = pyqtSignal(str)
    trigger_change_device_for_properties = pyqtSignal(dict)
    trigger_change_device_for_map = pyqtSignal(int)
    trigger_change_device_for_previews = pyqtSignal(int)

    def __init__(self, device_list):
        super().__init__()

        self.devices = device_list
        self.properties = self.devices[0].properties.keys()

        self.setSpacing(10)
        # self.setMinimumWidth(400)
        # self.setMaximumWidth(400)
        self.setMinimumHeight(200)

        for device in device_list:
            item = QListWidgetItem(device.title())
            self.addItem(item)

            # item = QListWidgetItem()
            # item.setSizeHint(QSize(300, 250))
            # widget = DeviceListItemWidget(device)
            # self.addItem(item)
            # self.setItemWidget(item, widget)

            item.setData(SIGNAL_PARAMETERS['DEVICE_ID'], device.device_id)
            if device.device_id == 0:
                print('first device selected, the url is: ' + device.stream_url)
                self.setCurrentItem(item)

        self.currentItemChanged.connect(self.change_device)
        self.itemDoubleClicked.connect(self.play)

    def change_device(self, current):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(self.currentRow())

    # TODO: May deliver the player_list[index](preview_list) directly to new window
    def play(self, item):
        player = Player(self.devices[self.currentRow()].stream_url)
        properties = PropertiesList(self.devices[self.currentRow()].properties)

        window_player = QMainWindow(self)

        widget = QWidget(self)
        widget.setGeometry(0, 0, 500, 300)
        window_player.setCentralWidget(widget)

        layout = QHBoxLayout()
        layout.addWidget(player)
        layout.addWidget(properties)
        widget.setLayout(layout)

        window_player.setAttribute(Qt.WA_DeleteOnClose)
        window_player.resize(1000, 700)
        window_player.show()

    def generate_item_widget(self, device: Device) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()

        layout.addWidget(QLabel(device.title()))
        for property in self.properties:
            if device.properties[property] is not None:
                label = QLabel(device.properties[property])
                label.resize()
                layout.addWidget(QLabel(device.properties[property]))
