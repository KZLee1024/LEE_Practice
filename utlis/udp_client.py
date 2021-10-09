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

        if len(recv_data) == 12:
            self.handle_recv_position(recv_data)
        elif len(recv_data) == 56:
            self.handle_recv_parameter(recv_data)

    def handle_recv_position(self, recv_data):
        recv_data = struct.unpack('iff', recv_data)
        print('message received', recv_data)

        device_index = recv_data[0]
        x = recv_data[1]
        y = recv_data[2]

        print((device_index, x, y))
        assert device_index >= 0 and x >= 0 and y >= 0
        self.trigger_move_device.emit(device_index, x, y)

    def handle_recv_parameter(self, recv_data):
        recv_data = struct.unpack('i9sf7sf7si5si', recv_data)
        print('message received', recv_data)

        device_index = recv_data[0]
        recv_data = recv_data[1:]

        pars = {}
        for index in range(len(global_pars.PARAMETER_KEYS)):
            key = recv_data[index*2].decode('utf-8')
            if global_pars.PARAMETER_KEYS.__contains__(key):
                pars[key] = recv_data[index*2+1]

        assert device_index >= 0
        self.trigger_update_parameter.emit(device_index, pars)
