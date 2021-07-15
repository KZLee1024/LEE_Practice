from enum import Enum


class DeviceType(Enum):
    undefined = -1
    UGV = 0  # Unmanned Ground Vehicle
    USV = 1  # Unmanned Surface Vehicle
    UAV = 2  # Unmanned Aerial Vehicle

    def text(self) -> str:
        if self.value == 0:
            return 'UGV'
        elif self.value == 1:
            return 'USV'
        elif self.value == 2:
            return 'UAV'
        else:
            return 'undefined'

    def icon_filename(self) -> str:
        if self.value == 0:
            return '/assets/icons/toy_car.svg'
        elif self.value == 1:
            return '/assets/icons/boat.svg'
        elif self.value == 2:
            return '/assets/icons/plane.svg'
        else:
            return 'undefined'


class Device:
    device_type: DeviceType = DeviceType.undefined
    device_id: int = -1
    stream_url = ""
    properties = {}
    coordinate: (float, float) = (0, 0)

    def __init__(self, device_type, device_id, url, properties, initial_coordinate):
        self.device_type = device_type
        self.device_id = device_id
        self.stream_url = url
        self.properties = properties
        self.coordinate = initial_coordinate

    def title(self) -> str:
        return self.device_type.text() + '-' + str(self.device_id)

    @staticmethod
    def sample() -> []:
        return [Device(DeviceType.UGV, 0, "http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8",
                       {"Loss Rate": "30%", "Latency": "50ms", "Channel": "2421MHz", "Power": "100mW"}, (0.3, 0.3)),
                Device(DeviceType.UGV, 1, "http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8",
                       {"Loss Rate": "27%", "Latency": "30ms", "Channel": "2421MHz", "Power": "100mW"}, (0.4, 0.8)),
                Device(DeviceType.UGV, 2, "http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8",
                       {"Loss Rate": "5%", "Latency": "5ms", "Channel": "2421MHz", "Power": "100mW"}, (0.7, 0.2)),
                Device(DeviceType.UGV, 3,
                       "https://dash.akamaized.net/dash264/TestCasesIOP33/adapatationSetSwitching/5/manifest.mpd",
                       {"Loss Rate": "100%", "Latency": "-", "Channel": "2421MHz", "Power": "100mW"}, (0.8, 0.6))]
