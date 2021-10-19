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
            return '/assets/icons/car.png'
        elif self.value == 1:
            return '/assets/icons/ship.png'
        elif self.value == 2:
            return '/assets/icons/UAV.png'
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
        return [
            Device(DeviceType.UGV, 0, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
                   {"Loss-Rate": "30", "Latency": "50", "Channel": "2421", "Power": "100"}, (300, 300)),
            Device(DeviceType.USV, 0, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
                   {"Loss-Rate": "27", "Latency": "30", "Channel": "2421", "Power": "100"}, (400, 800)),
            Device(DeviceType.UAV, 0, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
                   {"Loss-Rate": "5", "Latency": "5", "Channel": "2421", "Power": "100"}, (700, 200)),
            Device(DeviceType.UGV, 1, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
                   {"Loss-Rate": "100", "Latency": "-", "Channel": "2421", "Power": "100"}, (800, 600)),
            # Device(DeviceType.UGV, 1, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
            #        {"Loss-Rate": "100", "Latency": "-", "Channel": "2421", "Power": "100"}, (800, 600)),
            # Device(DeviceType.UGV, 1, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
            #        {"Loss-Rate": "100", "Latency": "-", "Channel": "2421", "Power": "100"}, (800, 600)),
            # Device(DeviceType.UGV, 1, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
            #        {"Loss-Rate": "100", "Latency": "-", "Channel": "2421", "Power": "100"}, (800, 600)),
            # Device(DeviceType.UGV, 1, "http://devimages.apple.com.edgekey.net/streaming/examples/bipbop_4x3/gear2/prog_index.m3u8",
            #        {"Loss-Rate": "100", "Latency": "-", "Channel": "2421", "Power": "100"}, (800, 600)),
        ]
