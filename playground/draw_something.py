import sys

from PyQt5.QtCore import QUrl, QTimer, QRect
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import matplotlib

import global_pars

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import threading
import random
import numpy as np


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        widget.setMaximumWidth(500)
        widget.setMinimumHeight(800)

        self.start_button = QPushButton('Start')
        self.end_button = QPushButton('end')
        self.start_button.clicked.connect(self.start_timer)
        self.end_button.clicked.connect(self.end_timer)

        self.timer = QTimer()
        self.timer.timeout.connect(self.draw)

        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)

        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.start_button)
        buttons_box.addWidget(self.end_button)

        layout = QVBoxLayout()
        layout.addLayout(buttons_box)
        layout.addWidget(self.canvas)

        widget.setLayout(layout)

        self.pars_label = global_pars.PARAMETER_KEYS
        self.data_lists = [[] for _ in range(4)]

        threading.Thread(target=self.push_data, daemon=True).start()

    def draw(self):
        print(self.data_lists)
        self.figure.clf()

        axes = self.figure.subplots(4, 1)

        for ax, data, label in zip(axes, self.data_lists, self.pars_label):
            ax.plot(data, color='g')
            ax.set_xlim(0, 30)
            ax.set_xticks([])
            ax.set_xlabel(label)

        self.canvas.draw()
        plt.grid(True)

    def start_timer(self):
        self.timer.start(50)
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(True)

    def end_timer(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.end_button.setEnabled(False)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def push_data(self):
        while True:
            pars = [random.randint(0, 100), random.randint(0, 100), int(random.random() * 2) + 2421,
                    100 + random.randint(0, 30)]
            print(pars)

            for data_list, data in zip(self.data_lists, pars):
                data_list.append(data)
                if len(data_list) > 30:
                    data_list.pop(0)

            time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = App()
    # w.show()
    terminal = Terminal()
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
