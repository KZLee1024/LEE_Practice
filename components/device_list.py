from PyQt5.QtCore import QEvent, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

SIGNAL_PARAMETERS = {'DEVICE_ID': 1}


class DeviceList(QListWidget):
    trigger_change_device_for_player = pyqtSignal(str)
    trigger_change_device_for_properties = pyqtSignal(dict)

    def __init__(self, device_list):
        super().__init__()

        self.devices = device_list

        self.setSpacing(10)
        # self.setMaximumWidth(200)
        for device in device_list:
            item = QListWidgetItem(device.device_title)
            # Add customized parameter 'deviceId' for index of '1'
            item.setData(SIGNAL_PARAMETERS['DEVICE_ID'], device.device_id)
            self.addItem(item)
            if device.device_id == 0:
                print('first device selected, url is: ' + device.device_url)
                self.setCurrentItem(item)

        self.currentItemChanged.connect(self.change_device)

    def change_device(self, current):
        print(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].device_url)
        self.trigger_change_device_for_player.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].device_url)
        self.trigger_change_device_for_properties.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].properties_list)
