import socket

client_address = ("172.30.21.205", 8888)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(device_index=0, x=50, y=50):
    global client_address

    input_data = input("input device_index,x and y (split by ' '): ")
    device_index, x, y = input_data.split(' ')
    print(device_index, x, y)

    if input_data == "EOF":
        udp_socket.sendto(input_data.encode('utf-8'), client_address)
        return 'EOF'

    send_data = 'devicePosition:'
    send_data = send_data + str(device_index)
    send_data = send_data + 'x:' + str(x)
    send_data = send_data + 'y:' + str(y)
    print(send_data)

    udp_socket.sendto(send_data.encode("utf-8"), client_address)


if __name__ == '__main__':
    while True:
        if send_message() == 'EOF':
            break
