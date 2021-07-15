from PyQt5.QtCore import QEvent, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

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
        index_of_list = 0
        for device in device_list:
            item = QListWidgetItem(device.title())
            # Add customized parameter 'deviceId' for index of '1'
            item.setData(SIGNAL_PARAMETERS['DEVICE_ID'], device.device_id)
            index_of_list += 1
            self.addItem(item)
            if device.device_id == 0:
                print('first device selected, the url is: ' + device.stream_url)
                self.setCurrentItem(item)

        self.currentItemChanged.connect(self.change_device)

    def change_device(self, current):
        # self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].stream_url)
        # self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties)
        self.trigger_change_device_for_map.emit(self.currentRow())
