import global_pars
from global_pars import CLIENT_HOST, CLIENT_PORT

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QUdpSocket


class UDPClient(QObject):
    trigger_move_device = pyqtSignal(int, int, int)         # device_index, x, y
    trigger_update_parameter = pyqtSignal(int, dict)    # device_

    def __init__(self):
        super().__init__()

        self.udp_client = QUdpSocket()
        self.udp_client.bind(CLIENT_PORT)
        self.udp_client.readyRead.connect(self.handle_recv)

    def handle_recv(self):
        buf, ip, port = self.udp_client.readDatagram(1024)
        recv_data = buf.decode('utf-8')
        print(recv_data)

        # =======过滤出字母和数字=========#
        # recv_data = filter(str.isalnum, str(recv_data))
        # recv_data = ''.join(list(recv_data))
        # print(recv_data)

        if recv_data.startswith('devicePosition'):
            self.handle_recv_position(recv_data)
        elif recv_data.startswith('deviceParameter'):
            self.handle_recv_parameter(recv_data)

    def handle_recv_position(self,  recv_data):
        recv_data = recv_data[len('devicePosition'):]
        print(recv_data)

        # TODO: regulate the dispatcher to send word split by ' '
        # ======= 获得坐标值 ========= #
        device_index = int(recv_data.split('x')[0])
        x = int(recv_data.split('x')[1].split('y')[0])
        y = int(recv_data.split('x')[1].split('y')[1])

        print((device_index, x, y))
        assert device_index >= 0 and x >= 0 and y >= 0
        self.trigger_move_device.emit(device_index, x, y)

    def handle_recv_parameter(self, recv_data):
        recv_data = recv_data[len('deviceParameter'):].split(' ')
        # print(recv_data)

        # ================== 获得属性key-value对 =================== #
        # ======= deviceParameter device_index key value ========= #
        device_index = int(recv_data[0])

        pars = {}
        for data in recv_data[1:]:
            data = data.split(':')
            if global_pars.PARAMETER_KEYS.__contains__(data[0]):
                pars[data[0]] = data[1]

        # print(device_index, pars)
        assert device_index >= 0
        self.trigger_update_parameter.emit(device_index, pars)





