from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize, QTimer
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import global_pars
from models.device import Device
from utlis.player import Player

import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import threading
import random
import numpy as np


# TODO: need a stop-event
class DeviceDetails(QMainWindow):
    def __init__(self, device_index, device: Device, initial_pars):
        super().__init__()

        self.device_index = device_index

        widget = QWidget()
        self.setCentralWidget(widget)

        # Stream_Player
        player_container = QLabel()
        # player_container.setMinimumWidth(2000)
        # player_container.setMinimumHeight(1500)
        player_container.setFixedSize(1000, 800)
        player_container.setText("")
        player_container.setObjectName("FullScreenVideo")

        threading.Thread(target=Player(container=player_container, device=device).display, daemon=True).start()

        # Properties_Drawer
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_properties)
        self.figure = plt.Figure()
        self.properties_canvas = FigureCanvas(self.figure)

        properties_container = QWidget()
        # properties_container.setMaximumWidth(800)
        properties_layout = QVBoxLayout()
        properties_layout.addWidget(self.properties_canvas)
        properties_container.setLayout(properties_layout)

        self.pars_label = global_pars.PARAMETER_KEYS
        self.data_lists = {}
        for label in self.pars_label:
            self.data_lists[label] = initial_pars[label]

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(player_container)
        layout.addWidget(properties_container)
        widget.setLayout(layout)

        self.start_timer()

    def draw_properties(self):
        self.figure.clf()

        axes = self.figure.subplots(4, 1)
        for ax, label in zip(axes, self.pars_label):
            ax.plot(self.data_lists[label], color='g')
            ax.set_xlim(0, 10)
            # ax.set_xticks([])
            ax.set_xlabel(label)

        self.properties_canvas.draw()
        plt.grid(True)

    def start_timer(self):
        self.timer.start(50)

    def end_timer(self):
        self.timer.stop()

    def push_data_handler(self, device_index, pars: dict):
        print('updating inside full-screen player', pars)
        if device_index == self.device_index:
            print(self.data_lists)
            for label in self.pars_label:
                self.data_lists[label].append(pars[label])
                if len(self.data_lists[label]) > 30:
                    print('poped')
                    self.data_lists[label].pop(0)
