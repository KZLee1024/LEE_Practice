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


# TODO: need a stop-event
class DeviceDetails(QMainWindow):
    trigger_close_device_detail = pyqtSignal(int)

    def __init__(self, device_index, device: Device, initial_pars):
        super().__init__()

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
        layout.addWidget(self.player_container)
        layout.addWidget(properties_container)
        widget.setLayout(layout)

        self.start_timer()

    def get_player_container(self):
        return self.player_container

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

    def closeEvent(self, event):
        """我们创建了一个消息框，上面有俩按钮：Yes和No.第一个字符串显示在消息框的标题栏，第二个字符串显示在对话框，
                    第三个参数是消息框的俩按钮，最后一个参数是默认按钮，这个按钮是默认选中的。返回值在变量reply里。"""

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if reply == QMessageBox.Yes:
            self.trigger_close_device_detail.emit(self.device_index)
            event.accept()
        else:
            event.ignore()
