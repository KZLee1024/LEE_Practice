import socket
import threading
import random
import time

# from utlis.arg_parser import getArg
from sys import argv
import struct


def getArg(flag, default=None):
    for i, v in enumerate(argv):
        if v == flag:
            if len(argv) < i + 2:
                break
            return argv[i + 1]
    return default


device_limit = int(getArg("-ld", 2))
message_limit = int(getArg("-lm", 50))

client_ip = getArg("-i", "127.0.0.1")
client_port = int(getArg("-p", 8888))

client_address = (client_ip, client_port)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_position_message(device_index=0):
    global client_address
    semaphore.acquire()

    for _ in range(message_limit):
        # Time Gap
        time.sleep(random.random() * 5)

        # input_data = input("input device_index,x and y (split by ' '): ")
        # device_index, x, y = input_data.split(' ')

        x = random.random() * 100
        y = random.random() * 100

        # send_data = [b'devicePosition:']
        send_data = [device_index, x, y]

        print(len(send_data), send_data)
        send_data = struct.pack('iff', send_data[0], send_data[1], send_data[2])
        udp_socket.sendto(send_data, client_address)
        print('message sent: ', send_data)

    semaphore.release()


LOSS_RATES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
LATENCY = [5, 10, 30, 50, 80]
CHANNEL = [2421]
POWER = [100, 110, 120, 130]


def send_parameters_message(device_index=0):
    global client_address
    semaphore.acquire()

    for _ in range(message_limit):
        # Time Gap
        time.sleep(1)

        send_data = []
        send_data.append(device_index)

        send_data.append('Loss-Rate'.encode('utf-8'))
        send_data.append(random.random() * 100)

        send_data.append('Latency'.encode('utf-8'))
        send_data.append(random.random() * 100)

        send_data.append('Channel'.encode('utf-8'))
        send_data.append(int(random.random() * 2) + 2421)

        send_data.append('Power'.encode('utf-8'))
        send_data.append(POWER[random.randint(0, 3)])

        print(len(send_data), send_data)
        send_data = struct.pack('i9sf7sf7si5si', send_data[0], send_data[1], send_data[2], send_data[3], send_data[4],
                                send_data[5], send_data[6], send_data[7], send_data[8])
        udp_socket.sendto(send_data, client_address)
        print('message sent: ', send_data)

    semaphore.release()


if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(device_limit)
    for i in range(device_limit):
        # threading.Thread(target=send_position_message, args=(i,)).start()
        threading.Thread(target=send_parameters_message, args=(i,)).start()


while threading.active_count() != 1:
    pass
else:
    print('---end---')
