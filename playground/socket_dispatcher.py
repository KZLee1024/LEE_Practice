import socket
import threading
import random
import time

from utlis.arg_parser import getArg


device_limit = int(getArg("-ld", 4))
message_limit = int(getArg("-lm", 10))

client_ip = getArg("-i", "172.30.21.205")
client_port = int(getArg("-p", 8888))

client_address = (client_ip, client_port)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(device_index=0):
    global client_address

    semaphore.acquire()

    for _ in range(message_limit):
        time.sleep(random.random()*20)

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


if __name__ == '__main__':
    semaphore = threading.BoundedSemaphore(device_limit)
    for i in range(device_limit):
        t = threading.Thread(target=send_message, args=(i,))
        t.start()


while threading.active_count() != 1:
    pass
else:
    print('---end---')