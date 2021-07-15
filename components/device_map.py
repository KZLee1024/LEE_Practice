from PyQt5.QtCore import QRect, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFrame, QInputDialog
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage, QMouseEvent

import global_pars

from models.device import Device, DeviceType


class DeviceMap(QWidget):
    device_list: [Device] = []
    label_list: [QLabel] = []
    selected_device_index = -1

    def __init__(self, device_list: [Device]):
        super().__init__()

        container = QWidget(self)
        container.setFixedSize(global_pars.MAP_WIDTH, global_pars.MAP_HEIGHT)

        container.setStyleSheet('QWidget{background-color: #ffffff}')
        # background.setStyleSheet("background-color: yellow;")

        button = QPushButton("Button")
        button.clicked.connect(self.move_to)

        layout = QVBoxLayout()
        layout.addWidget(container)
        layout.addWidget(button)

        self.setLayout(layout)

        self.device_list = device_list
        i = 0
        for device in self.device_list:
            img = None
            if device.device_type == DeviceType.UGV:
                img = QPixmap(global_pars.BASE_DIR + device.device_type.icon_filename())

            label = QLabel(container)
            label.setPixmap(img)
            # label.move(self.coordinate_transform(device.coordinate))
            label.move(10 * i, 10 * i)
            i += 1
            self.label_list.append(label)

        if len(self.device_list) > 0:
            self.selected_device_index = 0

        self.anim = None

    # enter the target coordinate and move
    def move_to(self):
        target_coordinate_x, ok_x = QInputDialog.getInt(self, 'Input Dialog', 'Enter x(0-100): ')
        target_coordinate_y, ok_y = QInputDialog.getInt(self, 'Input Dialog', 'Enter y(0-100): ')
        if ok_x and ok_y:
            print('moving...')
            self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"pos")
            self.anim.setDuration(1000)
            self.anim.setStartValue(self.label_list[self.selected_device_index].pos())
            self.anim.setEndValue(self.coordinate_transform(target_coordinate_x / 100, target_coordinate_y / 100))
            self.anim.start()

    # click and move
    def mousePressEvent(self, e: QMouseEvent) -> None:
        print('selected item: ', self.selected_device_index)
        print('selected item: ', self.label_list[self.selected_device_index])
        print('widget position: ', self.pos())
        print('press position: ', e.pos())

        self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"pos")
        self.anim.setDuration(1000)
        self.anim.setStartValue(self.label_list[self.selected_device_index].pos())
        self.anim.setEndValue(e.pos())
        self.anim.start()

    #  (0,0) ——————————————————— (wid,0)    #
    #    |                           |      #
    #    |                           |      #
    #    |                           |      #
    # (0,hei) —————————————————— (wid,hei)  #
    @staticmethod
    def coordinate_transform(target_coordinate_x: int, target_coordinate_y: int) -> QPoint:
        # Waiting for Coordinate Signal
        # return clickPos directly now
        return QPoint(target_coordinate_x, target_coordinate_y)

    def change_device_handler(self, new_index):
        print(new_index)
        self.selected_device_index = new_index
