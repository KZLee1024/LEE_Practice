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

        if recv_data.startswith('devicePosition:'):
            recv_data = recv_data[len('devicePosition:'):]
            print(recv_data)
            # =======过滤出字母和数字========= #
            recv_data = filter(str.isalnum, str(recv_data))
            recv_data = ''.join(list(recv_data))
            print(recv_data)
            # ======= 获得坐标值 ========= #
            device_index = int(recv_data[0])
            x = int(recv_data.split('x')[1].split('y')[0])
            y = int(recv_data.split('x')[1].split('y')[1])

            print((device_index, x, y))
            assert device_index >= 0 and x >= 0 and y >= 0
            self.trigger_move_device.emit(device_index, x, y)

#
# class UDPClient(QObject):
#     # ============== 创建套接字 ============== #
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#     # ============== 绑定一个本地地址 ============== #
#
#     local_addr = (CLIENT_HOST, CLIENT_PORT)
#     udp_socket.bind(local_addr)
#
#     trigger_move_device = pyqtSignal(int, int, int)
#
#     def recv_message(self):
#         while True:
#             device_index, x, y = -1, -1, -1
#             # ============== 接收数据 ============== #
#             recv_data, _ = self.udp_socket.recvfrom(1024)
#             recv_data = recv_data.decode('utf-8')
#             print(recv_data)
#
#             if recv_data.startswith('devicePosition:'):
#                 recv_data = recv_data[len('devicePosition:'):]
#                 print(recv_data)
#                 # =======过滤出字母和数字========= #
#                 recv_data = filter(str.isalnum, str(recv_data))
#                 recv_data = ''.join(list(recv_data))
#                 print(recv_data)
#                 # ======= 获得坐标值 ========= #
#                 device_index = int(recv_data[0])
#                 x = int(recv_data.split('x')[1].split('y')[0])
#                 y = int(recv_data.split('x')[1].split('y')[1])
#
#                 assert device_index > 0 and x > 0 and y > 0
#                 print((device_index, x, y))
#                 self.trigger_move_device.emit(device_index, x, y)
#
#             # For manually input message
#             if recv_data == 'EOF':
#                 self.udp_socket.close()
#                 return 'EOF'
#
#     thread_recv = Thread(target=recv_message)
#
#     def __init__(self):
#         super().__init__()
#         self.thread_recv.start()
#
#     def start(self):
#         self.thread_recv.start()
#
#     def end(self):
#         self.thread_recv.join()
#
#
# if __name__ == '__main__':
#     # t = threading.Thread(target=recv_message, args=())
#     # t.start()  # 开始线程
#     client = UDPClient()
#
#     while True:
#         if client.recv_message() == 'EOF':
#             break
