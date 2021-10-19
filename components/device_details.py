from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, pyqtSignal, QModelIndex, Qt, QUrl, QSize, QTimer
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
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
import pyqtgraph as pg


class DeviceDetails(QMainWindow):
    par_storage_limit = 100

    trigger_close_device_detail = pyqtSignal(int)

    def __init__(self, device_index, device: Device, initial_pars):
        super().__init__()
        print('############## initial_pars: ', initial_pars)

        self.device_index = device_index

        widget = QWidget()
        self.setCentralWidget(widget)

        # Stream_Player
        self.player_container = QLabel()
        # player_container.setMinimumWidth(2000)
        # player_container.setMinimumHeight(1500)
        self.player_container.setFixedSize(1000, 800)
        self.player_container.setText("")
        self.player_container.setObjectName("FullScreenVideo")

        # threading.Thread(target=Player(container=self.player_container, device=device).display, daemon=True).start()

        self.par_graphs = {}
        self.y_pars = {}
        for par_key in global_pars.PARAMETER_KEYS:
            self.y_pars[par_key] = list(initial_pars[par_key])
        self.x = list(range(len(self.y_pars[global_pars.PARAMETER_KEYS[0]])))
        self.data_line = {}

        graph_box = QVBoxLayout()
        line_pen = pg.mkPen(color=(255, 0, 0), width=3)
        for par_key in global_pars.PARAMETER_KEYS:
            graph_widget = pg.PlotWidget()
            graph_widget.setFixedSize(400, 200)
            graph_widget.setBackground('w')
            graph_widget.setLabel('bottom', '<span style=\"color:black;font-size:20px\">' + par_key + '</span>')
            graph_widget.showGrid(x=True, y=True)
            graph_widget.setXRange(0, self.par_storage_limit)

            self.par_graphs[par_key] = graph_widget
            self.data_line[par_key] = graph_widget.plot(self.x, self.y_pars[par_key], pen=line_pen)

            graph_box.addWidget(graph_widget)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.player_container)
        layout.addLayout(graph_box)
        widget.setLayout(layout)

    def get_player_container(self):
        return self.player_container

    def push_data_handler(self, device_index, pars: dict):
        if len(self.x) == 0:
            self.x.append(0)
        elif len(self.x) < self.par_storage_limit:
            self.x.append(self.x[-1]+1)

        if device_index == self.device_index:
            for label in global_pars.PARAMETER_KEYS:
                self.y_pars[label].append(pars[label])
                if len(self.y_pars[label]) > self.par_storage_limit:
                    self.y_pars[label].pop(0)
                self.data_line[label].setData(self.x, self.y_pars[label])

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.trigger_close_device_detail.emit(self.device_index)
            event.accept()
        else:
            event.ignore()
