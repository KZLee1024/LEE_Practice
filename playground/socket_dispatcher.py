import socket
import threading
import random
import time

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
        time.sleep(random.random() * 10)

        # input_data = input("input device_index,x and y (split by ' '): ")
        # device_index, x, y = input_data.split(' ')

        x = int(random.random() * 100)
        y = int(random.random() * 100)

        send_data = 'devicePosition:'
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
        # TODO: send all parameters or only the changed part?
        send_data = 'deviceParameter'
        send_data += str(device_index) + ' '

        send_data += 'Loss-Rate:'
        send_data += str(random.randint(0, 100)) + ' '

        send_data += 'Latency:'
        send_data += str(random.randint(0, 100)) + ' '

        send_data += 'Channel:'
        send_data += str(int(random.random()*2) + 2421) + ' '

        send_data += 'Power:'
        send_data += str(POWER[int(random.randint(0, 3))])

        udp_socket.sendto(send_data.encode("utf-8"), client_address)
        print('message sent: ', send_data)

    semaphore.release()


if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(device_limit)
    for i in range(device_limit):
        # t = threading.Thread(target=send_position_message, args=(i,))
        t = threading.Thread(target=send_parameters_message, args=(i,))
        t.start()

while threading.active_count() != 1:
    pass
else:
    print('---end---')
