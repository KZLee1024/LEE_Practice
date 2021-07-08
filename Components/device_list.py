from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class Device():
    deviceId: int = -1
    deviceTitle = ""
    deviceUrl = ""

    def __init__(self, id, title, url):
        self.deviceId = id
        self.deviceTitle = title
        self.deviceUrl = url


def generate_device_list() -> []:
    return [Device(0, "CCTV-1", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8"),
            Device(1, "CCTV-3", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8"),
            Device(2, "CCTV-5", "http://ivi.bupt.edu.cn/hls/cctv5hd.m3u8"),
            Device(3, "CCTV-6", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8"),
            Device(4, "dash", "https://dash.akamaized.net/dash264/TestCasesIOP33/adapatationSetSwitching/5/manifest.mpd")]


class DeviceList(QListWidget):
    def __init__(self):
        super().__init__()
        deviceList = generate_device_list()

        self.setSpacing(20)
        self.setMaximumWidth(200)
        for device in deviceList:
            item = QListWidgetItem(device.deviceTitle)
            self.addItem(item)
            if device.deviceId == 0:
                self.setCurrentItem(item)

