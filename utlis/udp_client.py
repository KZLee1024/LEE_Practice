# from glob import glob
# import socket
# from threading import Thread
# from global_pars import CLIENT_HOST, CLIENT_PORT
#
# from PyQt5.QtCore import pyqtSignal, QObject
# from PyQt5.QtNetwork import QUdpSocket
#
#
#
# class UDPClient(QObject):
#     trigger_move_device = pyqtSignal(int, int, int)
#
#     def __init__(self):
#         super().__init__()
#
#         # ============== 创建套接字 ============== #
#         self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         # ============== 绑定一个本地地址 ============== #
#         self.host = socket.gethostname()
#         self.port = 8888
#         self.local_addr = (self.host, self.port)
#         self.udp_socket.bind(self.local_addr)
#
#     def handle_recv(self):
#         recv_data, _ = self.udp_socket.recvfrom(1024)
#         recv_data = recv_data.decode('utf-8')
#         print(recv_data)
#         if recv_data.startswith('d'):
#             # =======过滤出字母和数字========= #
#             recv_data = filter(str.isalnum, str(recv_data))
#             recv_data = ''.join(list(recv_data))
#             recv_data = recv_data[len('devicePosition'):]
#
#             # ======= 获得坐标值 ========= #
#             device_index = int(recv_data[0])
#             x = int(recv_data.split('x')[1].split('y')[0])
#             y = int(recv_data.split('x')[1].split('y')[1])
#             print((device_index, x, y))
#             assert device_index >= 0 and x >= 0 and y >= 0
#             self.trigger_move_device.emit(device_index, x, y)
#
from glob import glob
import socket
from threading import Thread
from global_pars import CLIENT_HOST, CLIENT_PORT

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtNetwork import QUdpSocket


class UDPClient(QObject):
    trigger_move_device = pyqtSignal(int, int, int)

    def __init__(self):
        super().__init__()

        self.udp_client = QUdpSocket()
        self.udp_client.bind(CLIENT_PORT)
        self.udp_client.readyRead.connect(self.handle_recv)

    def handle_recv(self):
        buf = bytes()
        buf, ip, port = self.udp_client.readDatagram(1024)
        recv_data = buf.decode('utf-8')
        print(recv_data)
        # =======过滤出字母和数字=========#
        recv_data = filter(str.isalnum, str(recv_data))
        recv_data = ''.join(list(recv_data))
        print(recv_data)
        if recv_data.startswith('d'):
            recv_data = recv_data[len('devicePosition'):]
            print(recv_data)

            # ======= 获得坐标值 ========= #
            device_index = int(recv_data[0])
            x = int(recv_data.split('x')[1].split('y')[0])
            y = int(recv_data.split('x')[1].split('y')[1])

            print((device_index, x, y))
            assert device_index >= 0 and x >= 0 and y >= 0
            self.trigger_move_device.emit(device_index, x, y)

