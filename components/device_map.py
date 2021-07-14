from PyQt5.QtCore import QRect, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage

import PyQt5.Qt

import global_pars


class DeviceMap(QWidget):
    def __init__(self, device_list):
        super().__init__()

        container = QWidget(self)
        container.setFixedSize(global_pars.MAP_WIDTH, global_pars.MAP_HEIGHT)

        container.setStyleSheet('QWidget{background-color: #ffffff}')
        # background.setStyleSheet("background-color: yellow;")

        button = QPushButton("Button")
        button.clicked.connect(self.do_anim)

        layout = QVBoxLayout()
        layout.addWidget(container)
        layout.addWidget(button)

        self.setLayout(layout)

        self.label = QLabel(container)
        device0 = QPixmap(global_pars.BASE_DIR + "/assets/icons/toy_car.svg")
        self.label.setPixmap(device0)

        self.anim = None

    def do_anim(self):
        self.anim = QPropertyAnimation(self.label, b"pos")
        self.anim.setDuration(100)
        self.anim.setStartValue(self.label.pos())
        self.anim.setEndValue(QPoint(self.label.pos().x() + 100, self.label.pos().y()+50))
        self.label.rect().adjust(10, 10, 10, 10)
        self.anim.start()
