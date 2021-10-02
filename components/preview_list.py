import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QLabel, QScrollArea, QGridLayout

from utlis.player import Player


class PreviewList(QScrollArea):
    previews = []
    selected_preview_index = -1

    def __init__(self, devices):
        super().__init__()
        self.devices = devices

        self.setMinimumWidth(795)
        self.setMaximumWidth(795)
        self.scroll_container = QWidget()

        layout = QGridLayout()
        layout.setSpacing(0)
        row, col = 0, 0

        for index in range(len(self.devices)):
            new_preview = QLabel()
            new_preview.setFixedSize(360, 320)
            # new_preview.setMinimumWidth(360)
            # new_preview.setMaximumWidth(360)
            # new_preview.setMinimumHeight(320)
            # new_preview.setMaximumHeight(320)
            new_preview.setText("")
            new_preview.setObjectName("video-" + str(index))

            label = QLabel(self.devices[index].title())
            h_box = QHBoxLayout()
            h_box.addStretch(1)
            h_box.addWidget(label)
            h_box.addStretch(1)

            layout_container_preview = QVBoxLayout()
            layout_container_preview.addWidget(new_preview)
            layout_container_preview.addLayout(h_box)

            widget = QWidget()
            widget.setLayout(layout_container_preview)
            widget.setAutoFillBackground(True)

            layout.addWidget(widget, row, col)
            self.previews.append(widget)

            threading.Thread(target=Player(container=new_preview, device=self.devices[index]).display, daemon=True).start()

            if index % 2 == 0:
                col = 1
            else:
                col = 0
                row += 1

        if len(self.previews) > 0:
            self.change_device_handler(0)

        print(len(self.previews))
        print(self.previews[0])
        self.scroll_container.setLayout(layout)

        self.setWidget(self.scroll_container)
        self.scroll_container.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(self.scroll_container.backgroundRole(), Qt.transparent)
        self.scroll_container.setPalette(palette)

    def change_device_handler(self, new_index):
        if self.selected_preview_index != -1:
            palette = self.previews[self.selected_preview_index].palette()
            palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.transparent)
            self.previews[self.selected_preview_index].setPalette(palette)

        self.selected_preview_index = new_index

        palette = self.previews[self.selected_preview_index].palette()
        palette.setColor(self.previews[self.selected_preview_index].backgroundRole(), Qt.red)
        self.previews[self.selected_preview_index].setPalette(palette)
