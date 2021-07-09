from PyQt5.QtCore import QEvent, pyqtSignal
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

SIGNAL_PARAMETERS = {'DEVICE_ID': 1}


class DeviceList(QListWidget):
    trigger_change_device = pyqtSignal(str)

    def __init__(self, device_list):
        super().__init__()

        self.devices = device_list

        self.setSpacing(20)
        self.setMaximumWidth(200)
        for device in device_list:
            item = QListWidgetItem(device.deviceTitle)
            # Add customized parameter 'deviceId' for index of '1'
            item.setData(SIGNAL_PARAMETERS['DEVICE_ID'], device.deviceId)
            self.addItem(item)
            if device.deviceId == 0:
                print('first device selected, url is: ' + device.deviceUrl)
                self.setCurrentItem(item)

        self.currentItemChanged.connect(self.change_device)

    def change_device(self, current):
        print(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].deviceUrl)
        self.trigger_change_device.emit(self.devices[current.data(SIGNAL_PARAMETERS['DEVICE_ID'])].deviceUrl)
