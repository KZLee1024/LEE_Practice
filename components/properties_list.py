from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem


class PropertiesList(QListWidget):
    def __init__(self, default_properties):
        super().__init__()

        self.setSpacing(10)
        self.setMaximumWidth(200)

        self.update_list(default_properties)

    def update_list(self, properties_list):
        self.clear()
        for key, value in properties_list.items():
            item = QListWidgetItem(key + ": " + value)
            self.addItem(item)




