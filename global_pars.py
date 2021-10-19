import os
import socket

BASE_DIR = os.path.dirname(__file__)

# MAP_WIDTH = 1020
# MAP_HEIGHT = 750

BASE_WIDTH = 650
BASE_HEIGHT = 350
scale = 1.5
MAP_WIDTH = BASE_WIDTH * scale
MAP_HEIGHT = BASE_HEIGHT * scale

CLIENT_HOST = socket.gethostname()
CLIENT_PORT = 8888

PARAMETER_KEYS = ["Loss-Rate", "Latency", "Channel", "Power"]