from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage

import PyQt5.Qt

import global_pars


class DeviceMap(QWidget):
    def __init__(self, device_list):
        super().__init__()

        # TODO: Animations

        container = QWidget(self)
        container.setFixedSize(global_pars.MAP_WIDTH, global_pars.MAP_HEIGHT)

        container.setStyleSheet('QWidget{background-color: #ffffff}')
        # background.setStyleSheet("background-color: yellow;")

        layout = QVBoxLayout()
        layout.addWidget(container)

        self.setLayout(layout)

        label = QLabel(container)
        device0 = QPixmap(global_pars.BASE_DIR + "/assets/icons/toy_car.svg")
        label.setPixmap(device0)

