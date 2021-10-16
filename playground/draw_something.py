import sys
import time

from PyQt5.QtCore import QUrl, QTimer, QRect, QPointF
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton, \
    QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import global_pars
from models.device import Device
from utlis.player import Player

import threading
import random
import numpy as np

device = Device.sample()[0]


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.player_container = QLabel()
        self.player_container.setFixedSize(800, 600)
        self.player_container.setText("")
        self.player_container.setObjectName("FullScreenVideo")

        self.start_button = QPushButton('Start')
        # self.end_button = QPushButton('end')

        self.start_button.clicked.connect(self.start_push)
        # self.end_button.clicked.connect(self.end_push)

        self.graphs = {}
        self.x = []
        self.y_pars = {}
        self.data_line = {}

        line_pen = pg.mkPen(color=(255, 0, 0), width=5)
        for key in global_pars.PARAMETER_KEYS:
            graph_widget = pg.PlotWidget()
            graph_widget.setFixedSize(200, 200)
            graph_widget.setBackground('w')
            graph_widget.setLabel('bottom', '<span style=\"color:black;font-size:20px\"> Loss-Rate </span>')
            graph_widget.showGrid(x=True, y=True)
            graph_widget.setXRange(0, 30)

            self.graphs[key] = graph_widget
            self.y_pars[key] = []
            self.data_line[key] = graph_widget.plot(self.x, self.y_pars[key], pen=line_pen)

        buttons_box = QHBoxLayout()
        buttons_box.addWidget(self.start_button)
        # buttons_box.addWidget(self.end_button)

        v_box = QVBoxLayout()
        v_box.addLayout(buttons_box)
        for key in self.graphs:
            v_box.addWidget(self.graphs[key])

        layout = QHBoxLayout()
        layout.addWidget(self.player_container)
        layout.addLayout(v_box)
        widget.setLayout(layout)

        player = Player(container=self.player_container, device=device)

        threading.Thread(target=player.display, daemon=True).start()
        self.push_data_thread = threading.Thread(target=self.push_data, daemon=True)

    def start_push(self):
        self.push_data_thread.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def push_data(self):
        for _ in range(50):
            pars = [random.randint(0, 100), random.randint(0, 100), int(random.random() * 2) + 2421,
                    100 + random.randint(0, 30)]
            print(pars)

            if len(self.x) == 0:
                self.x.append(0)
            elif len(self.x) < 30:
                self.x.append(self.x[-1]+1)

            for index, key in enumerate(global_pars.PARAMETER_KEYS):
                self.y_pars[key].append(pars[index])
                if len(self.y_pars[key]) > 30:
                    self.y_pars[key].pop(0)

                self.data_line[key].setData(self.x, self.y_pars[key])

            time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = App()
    # w.show()
    terminal = Terminal()
    terminal.center()
    terminal.show()
    sys.exit(app.exec_())
