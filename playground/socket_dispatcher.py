import socket
import threading
import random
import time
import struct

# from utlis.arg_parser import getArg
from sys import argv


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
        # time.sleep(random.random() * 20)
        time.sleep(3)

        # input_data = input("input device_index,x and y (split by ' '): ")
        # device_index, x, y = input_data.split(' ')

        x = int(random.random() * 650)
        y = int(random.random() * 350)

        send_data = 'position'
        send_data = send_data + str(device_index)
        send_data = send_data + 'x:' + str(x)
        send_data = send_data + 'y:' + str(y)

        udp_socket.sendto(send_data.encode("utf-8"), client_address)
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
        time.sleep(1)
        deviceParameter = device_index
        Packloss = random.randint(0, 100) + 0.1
        Latency = random.randint(0, 100) + 0.1
        Channel = int(random.random() * 2) + 2421
        Power = POWER[int(random.randint(0, 3))]

        send_data = "videoifo".encode() + struct.pack("iffii", deviceParameter, Packloss, Latency, Channel, Power)
        udp_socket.sendto(send_data, client_address)
        detail = struct.unpack("iffii", send_data[8:len(send_data)])
        print("videoinfo:", detail)
    semaphore.release()


def send_detect_message(device_index=0):
    global client_address
    semaphore.acquire()

    for _ in range(message_limit):
        time.sleep(1)
        results = []
        name = "car"
        results.append(1)
        results.append(0.95)
        results.append(50.5)
        results.append(20)
        results.append(30)
        results.append(40)
        results.append(50)

        send_data = "detectif".encode() + struct.pack("i", len(name)) + name.encode() + struct.pack("iffiiii",
                                                                                                    results[0],
                                                                                                    results[1],
                                                                                                    results[2],
                                                                                                    results[3],
                                                                                                    results[4],
                                                                                                    results[5],
                                                                                                    results[6])

        udp_socket.sendto(send_data, client_address)

        name_len = struct.unpack("i", send_data[8:12])
        name2 = send_data[12:12 + name_len[0]].decode()
        detail = struct.unpack("ifiiiii", send_data[12 + name_len[0]:len(send_data)])
        device_index = detail[0]
        accuracy = detail[1]
        distance = detail[2]
        print("detectinfo:", name_len, name2, detail)

    semaphore.release()


if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(device_limit)
    for i in range(device_limit):
        w = threading.Thread(target=send_position_message, args=(i,), daemon=True)
        t = threading.Thread(target=send_parameters_message, args=(i,), daemon=True)
        z = threading.Thread(target=send_detect_message, args=(i,), daemon=True)
        # z.start()
        # t.start()
        w.start()

while threading.active_count() != 1:
    pass
else:
    print('---end---')
