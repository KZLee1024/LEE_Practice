import socket

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(x=0.5, y=0.5):
    send_data = input("input plz: ")
    if send_data == "exit":
        return 'EOF'

    udp_socket.sendto(send_data.encode("utf-8"), ("172.30.21.219", 8888))


if __name__ == '__main__':
    while True:
        if send_message() == 'EOF':
            break
