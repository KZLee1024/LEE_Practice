from enum import Enum


class DeviceType(Enum):
    undefined = -1
    UGV = 0  # Unmanned Ground Vehicle
    USV = 1  # Unmanned Surface Vehicle
    UAV = 2  # Unmanned Aerial Vehicle

    def text(self) -> str:
        if self == 0:
            return 'Unmanned Ground Vehicle'
        elif self == 1:
            return 'Unmanned Surface Vehicle'
        elif self == 2:
            return 'Unmanned Aerial Vehicle'
        else:
            return 'undefined'


class Device:
    device_type: DeviceType = -1
    device_id: int = -1
    device_title = ""
    device_url = ""

    def __init__(self, type, device_id, title, url, properties):
        self.device_type = type
        self.device_id = device_id
        self.device_title = title
        self.device_url = url
        self.properties_list = properties

    @staticmethod
    def sample() -> []:
        return [Device(0, 0, "CCTV-1", "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8",
                       {"Loss Rate": "30%", "Latency": "50ms", "Channel": "2421MHz", "Power": "100mW"}),
                Device(0, 1, "CCTV-3", "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8",
                       {"Loss Rate": "27%", "Latency": "30ms", "Channel": "2421MHz", "Power": "100mW"}),
                Device(0, 2, "CCTV-6", "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8",
                       {"Loss Rate": "5%", "Latency": "5ms", "Channel": "2421MHz", "Power": "100mW"}),
                Device(0, 3, "dash",
                       "https://dash.akamaized.net/dash264/TestCasesIOP33/adapatationSetSwitching/5/manifest.mpd",
                       {"Loss Rate": "100%", "Latency": "-", "Channel": "2421MHz", "Power": "100mW"})]
