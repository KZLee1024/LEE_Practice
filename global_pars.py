import os
import socket

BASE_DIR = os.path.dirname(__file__)

# MAP_WIDTH = 1020
# MAP_HEIGHT = 750
MAP_WIDTH = 800
MAP_HEIGHT = 800

CLIENT_HOST = socket.gethostname()
CLIENT_PORT = 8888

PARAMETER_KEYS = ["Loss-Rate", "Latency", "Channel", "Power"]