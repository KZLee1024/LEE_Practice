from PyQt5.QtCore import QRect, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFrame, QInputDialog
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage, QMouseEvent, QPalette
from PyQt5.QtCore import Qt

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

        button_move = QPushButton("Move To")
        button_move.clicked.connect(self.move_to)
        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(button_move)

        layout = QVBoxLayout()
        layout.addWidget(container)
        layout.addLayout(h_box)

        self.setLayout(layout)

        self.device_list = device_list
        for device in self.device_list:
            pixmap = QPixmap(global_pars.BASE_DIR + device.device_type.icon_filename())

            label = QLabel(container)
            label.setPixmap(pixmap)
            label.setGeometry(QRect(self.coordinate_transform(device.coordinate[0], device.coordinate[1]), QSize(30, 30)))
            label.setScaledContents(True)
            label.setAutoFillBackground(True)
            label.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)
            # label.move(self.coordinate_transform(device.coordinate[0], device.coordinate[1]))
            self.label_list.append(label)

        if len(self.device_list) > 0:
            self.change_device_handler(0)

        self.anim = None

    # enter the target coordinate and move
    def move_to(self):
        target_coordinate_x, ok_x = QInputDialog.getDouble(self, 'Input Dialog', 'Enter x(0.0-1.0): ')
        if ok_x:
            target_coordinate_y, ok_y = QInputDialog.getDouble(self, 'Input Dialog', 'Enter y(0.0-1.0): ')
            if ok_y:
                print('moving...')
                self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"pos")
                self.anim.setDuration(1000)
                self.anim.setStartValue(self.label_list[self.selected_device_index].pos())
                self.anim.setEndValue(
                    self.coordinate_transform(target_coordinate_x, target_coordinate_y))
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
    def coordinate_transform(self, target_coordinate_x: float, target_coordinate_y: float) -> QPoint:
        # Waiting for Coordinate Signal
        # return clickPos directly now
        return QPoint(int(self.geometry().width() * target_coordinate_x), int(self.geometry().height() * target_coordinate_y))

    def change_device_handler(self, new_index):
        if self.selected_device_index != -1:
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.green)
            point = self.label_list[self.selected_device_index].pos()
            self.label_list[self.selected_device_index].setGeometry(QRect(point, QSize(30, 30)))
            self.label_list[self.selected_device_index].setPalette(pe)
        print('new index: ', new_index)
        self.selected_device_index = new_index
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.green)
        point = self.label_list[self.selected_device_index].pos()
        self.label_list[self.selected_device_index].setGeometry(QRect(point, QSize(70, 70)))
        self.label_list[self.selected_device_index].setPalette(pe)

    def move_device_handler(self, device_index, x, y):
        self.anim = QPropertyAnimation(self.label_list[device_index], b"pos")
        self.anim.setDuration(1000)
        self.anim.setStartValue(self.label_list[device_index].pos())
        self.anim.setEndValue(self.coordinate_transform(x/100, y/100))
        self.anim.start()
