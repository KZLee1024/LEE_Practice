import struct

import global_pars
from global_pars import CLIENT_HOST, CLIENT_PORT

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QUdpSocket


class UDPClient(QObject):
    trigger_move_device = pyqtSignal(int, int, int)  # device_index, x, y
    trigger_update_parameter = pyqtSignal(int, dict)  # device_

    def __init__(self):
        super().__init__()

        self.udp_client = QUdpSocket()
        self.udp_client.bind(CLIENT_PORT)
        self.udp_client.readyRead.connect(self.handle_recv)

    def handle_recv(self):
        recv_data, ip, port = self.udp_client.readDatagram(1024)

        prefix=recv_data[0:8].decode()


        if prefix == "position":
            self.handle_recv_position(recv_data)
        elif prefix == "videoifo":
            self.handle_recv_parameter(recv_data)
        elif prefix == "detectif":
            self.handle_recv_detct(recv_data)


    def handle_recv_position(self, recv_data1):
        recv_data=recv_data1.decode('utf-8')
        print(recv_data)
        recv_data = filter(str.isalnum, str(recv_data))
        recv_data = ''.join(list(recv_data))
        print(recv_data)
        if recv_data.startswith('p'):
            recv_data = recv_data[len('position'):]
            print(recv_data)

            # ======= 获得坐标值 ========= #
            device_index = int(recv_data[0])
            x = int(recv_data.split('x')[1].split('y')[0])
            y = int(recv_data.split('x')[1].split('y')[1])

            print((device_index, x, y))
            assert device_index >= 0 and x >= 0 and y >= 0
            self.trigger_move_device.emit(device_index, x, y)

    def handle_recv_parameter(self, recv_data):
        detail=struct.unpack("iffii", recv_data[8:len(recv_data)])
        print("videoinfo:",detail)

        device_index = detail[0]

    def handle_recv_detct(self, recv_data):
        name_len = struct.unpack("i", recv_data[8:12])
        name2 = recv_data[12:12 + name_len[0]].decode()
        detail=struct.unpack("iffiiii", recv_data[12 + name_len[0]:len(recv_data)])
        device_index=detail[0]
        accuracy=detail[1]
        distance=detail[2]


        print("detectinfo:",name_len,name2,detail)
