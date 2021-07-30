from glob import glob
import socket
import threading

# def main():
#     path = 'E:\Data\ID0'
#     txts = glob(path + '/*')
#     txts.sort()
#     print(txts[-2])
#     lines = open(txts[-2], 'r', encoding='UTF-8').readlines()
#     print(lines)

# ============== 创建套接字 ============== #
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ============== 绑定一个本地地址 ============== #
host = socket.gethostname()
port = 8888
local_addr = (host, port)
udp_socket.bind(local_addr)


# localaddr = ("172.30.21.219", 8888)
# udp_socket.bind(localaddr)

def recv_message():
    device_index, x, y = -1, -1, -1
    # ============== 接收数据 ============== #
    recv_data, _ = udp_socket.recvfrom(1024)
    recv_data = recv_data.decode('utf-8')
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


    if recv_data == 'EOF':
        udp_socket.close()
        return 'EOF'



def main():
    while True:
        recv_data, _ = udp_socket.recvfrom(1024)
        recv_data = recv_data.decode('utf-8')

        print(recv_data)
        if recv_data == "EOF":
            break

    udp_socket.close()


if __name__ == '__main__':
    # t = threading.Thread(target=recv_message, args=())
    # t.start()  # 开始线程
    while True:
        if recv_message() == 'EOF':
            break
