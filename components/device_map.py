from PyQt5.QtCore import QRect, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFrame, QInputDialog
from PyQt5.QtGui import QPixmap, QColor, QIcon, QImage, QMouseEvent, QPalette, QBrush
from PyQt5.QtCore import Qt

import global_pars

from models.device import Device, DeviceType

class DeviceMap(QWidget):
    device_list: [Device] = []
    label_list: [QWidget] = []
    selected_device_index = -1

    def __init__(self, device_list: [Device]):
        super().__init__()
        self.count = 1
        self.container = QWidget(self)
        self.container.setAutoFillBackground(True)
        self.container.setFixedSize(global_pars.MAP_WIDTH, global_pars.MAP_HEIGHT)

        # container.setStyleSheet('QWidget{background-image: ' + global_pars.BASE_DIR + '/assets/imgs/map-background.jpg}')
        # background.setStyleSheet("background-color: yellow;")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(global_pars.BASE_DIR + "/assets/imgs/map-background.jpg")))
        self.container.setPalette(palette)

        # button_move = QPushButton("Move To")

        button_hide = QPushButton("地图显示功能")
        button_hide.setStyleSheet("color:white;font-size:20px;font-family:Roman times;background-color:darkcyan;")
        button_hide.clicked.connect(self.hide_map)
        h_box = QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(button_hide)

        layout = QVBoxLayout()
        layout.addWidget(self.container)
        layout.addLayout(h_box)

        self.setLayout(layout)

        self.device_list = device_list
        for device in self.device_list:
            pixmap = QPixmap(global_pars.BASE_DIR + device.device_type.icon_filename())

            widget = QWidget(self.container)
            layout = QVBoxLayout()
            layout.setSpacing(0)

            label_pix = QLabel()
            label_pix.setPixmap(pixmap)
            label_pix.setScaledContents(True)
            label_pix.setAlignment(Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignTop)

            label_text = QLabel()
            label_text.setText(device.title())
            label_text.setScaledContents(True)
            label_text.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
            label_text.setMaximumHeight(20)

            layout.addWidget(label_pix)
            layout.addWidget(label_text)
            widget.setLayout(layout)
            widget.resize(70, 90)

            widget.move(self.coordinate_transform(device.coordinate[0], device.coordinate[1]))
            self.label_list.append(widget)


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

    def hide_map(self):
        if self.count % 2 != 0:
            self.container.setHidden(True)
        else:
            self.container.setHidden(False)
        self.count += 1

    # click and move
    def mousePressEvent(self, e: QMouseEvent) -> None:
        print('selected item: ', self.selected_device_index)
        print('selected item: ', self.label_list[self.selected_device_index])
        print('widget position: ', self.pos())
        print('press position: ', e.pos())

        target = e.pos()
        canvas = self.geometry()
        self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"pos")
        self.anim.setDuration(1000)
        self.anim.setStartValue(self.label_list[self.selected_device_index].pos())
        self.anim.setEndValue(self.coordinate_transform(target.x()/canvas.width(), target.y()/canvas.height()))
        self.anim.start()

    #  (0,0) ——————————————————— (wid,0)    #
    #    |                           |      #
    #    |                           |      #
    #    |                           |      #
    # (0,hei) —————————————————— (wid,hei)  #
    def coordinate_transform(self, target_coordinate_x: float, target_coordinate_y: float) -> QPoint:
        # Waiting for Coordinate Signal
        # return clickPos directly now
        if target_coordinate_x > 0.85:
            target_coordinate_x = 0.85
        if target_coordinate_y > 0.8:
            target_coordinate_y = 0.8

        return QPoint(int(self.geometry().width() * target_coordinate_x), int(self.geometry().height() * target_coordinate_y))

    def change_device_handler(self, new_index):
        if self.selected_device_index != -1:
            self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"size")
            self.anim.setDuration(100)
            self.anim.setStartValue(self.label_list[self.selected_device_index].size())
            self.anim.setEndValue(QSize(70, 90))
            self.anim.start()
            # point = self.label_list[self.selected_device_index].pos()
            self.label_list[self.selected_device_index].resize(QSize(70, 90))
            pe = QPalette()
            pe.setColor(QPalette.WindowText, Qt.black)
            self.label_list[self.selected_device_index].setPalette(pe)
        print('new index: ', new_index)
        self.selected_device_index = new_index
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.anim = QPropertyAnimation(self.label_list[self.selected_device_index], b"size")
        self.anim.setDuration(100)
        self.anim.setStartValue(self.label_list[self.selected_device_index].size())
        self.anim.setEndValue(QSize(90, 110))
        self.anim.start()
        self.label_list[self.selected_device_index].setPalette(pe)

    def move_device_handler(self, device_index, x, y):
        self.anim = QPropertyAnimation(self.label_list[device_index], b"pos")
        self.anim.setDuration(2000)
        self.anim.setStartValue(self.label_list[device_index].pos())
        self.anim.setEndValue(self.coordinate_transform(x/100, y/100))
        self.anim.start()
