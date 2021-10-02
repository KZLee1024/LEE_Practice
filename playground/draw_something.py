import sys

from PyQt5.QtCore import QUrl, QTimer, QRect
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import matplotlib

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

        widget.setFixedSize(800, 600)

        self.start_button = QPushButton('Start')
        self.end_button = QPushButton('end')
        self.start_button.clicked.connect(self.start_timer)
        self.end_button.clicked.connect(self.end_timer)

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        h_box = QHBoxLayout()
        h_box.addWidget(self.start_button)
        h_box.addWidget(self.end_button)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(h_box)

        widget.setLayout(layout)

        self.num_a_list = []
        self.num_b_list = []
        self.num_c_list = []

    def show_time(self):
        ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])

        ax.clear()
        ax.plot(self.num_a_list, label='A', linestyle=':', color='g')
        ax.plot(self.num_b_list, label='B', linestyle='--', color='b')
        ax.plot(self.num_c_list, label='C', linestyle='-.', color='r')

        self.figure.legend()
        self.canvas.draw()
        plt.grid(True)

    def start_timer(self):
        self.timer.start(100)
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(True)

    def end_timer(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.end_button.setEnabled(False)

        self.num_a_list = []
        self.num_b_list = []
        self.num_c_list = []

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class App(QWidget):
    def __init__(self, parent=None):
        # 父类初始化方法
        super(App, self).__init__(parent)
        self.initUI()
        self.center()

        threading.Thread(target=self.getData, daemon=True).start()

    def initUI(self):
        self.setWindowTitle('数据可视化')
        self.setFixedSize(1000, 600)
        # 几个QWidgets

        self.startBtn = QPushButton('开始')
        self.endBtn = QPushButton('结束')
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        # 图像模块
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        # 垂直布局

        # x = np.linspace(0, np.pi)
        # y_sin = np.sin(x)
        # y_cos = np.cos(x)
        #
        # ax = self.figure.add_subplot(221)
        # ax.plot(x, y_sin)
        # ax.plot(x, y_cos)

        layout = QVBoxLayout()
        layout.addWidget(self.startBtn)
        layout.addWidget(self.endBtn)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # 数组初始化
        self.people_num_list = [-1 for _ in range(30)]
        self.cars_num_list = []
        self.motors_num_list = []

    def center(self, screenNum=0):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.normalGeometry2 = QRect((screen.width() - size.width()) / 2 + screen.left(),
                                     (screen.height() - size.height()) / 2,
                                     size.width(), size.height())
        self.setGeometry((screen.width() - size.width()) / 2 + screen.left(),
                         (screen.height() - size.height()) / 2,
                         size.width(), size.height())

    def showTime(self):
        # shuju=np.random.random_sample()*10#返回一个[0,1)之间的浮点型随机数*10
        # shuju_2=np.random.random_sample()*10#返回一个[0,1)之间的浮点型随机数*10
        # self.x.append(shuju)#数组更新
        # self.xx.append(shuju_2)

        ax = self.figure.add_subplot(111)

        ax.clear()
        ax.plot(range(30), self.people_num_list, label="people_num", linestyle='-', color="g")
        # ax.plot(self.cars_num_list, label="cars_num", color="b", linestyle='--')
        # ax.plot(self.motors_num_list, label="motors_num", color="r", linestyle='-')

        # self.figure.legend()
        self.canvas.draw()
        plt.grid(True)

    # 启动函数
    def startTimer(self):
        # 设置计时间隔并启动
        self.timer.start(50)  # 每隔一秒执行一次绘图函数 showTime
        self.startBtn.setEnabled(False)  # 开始按钮变为禁用
        self.endBtn.setEnabled(True)  # 结束按钮变为可用

    def endTimer(self):
        self.timer.stop()  # 计时停止
        self.startBtn.setEnabled(True)  # 开始按钮变为可用
        self.endBtn.setEnabled(False)  # 结束按钮变为可用
        self.people_num_list = [-1 for _ in range(30)]
        self.cars_num_list = []
        self.motors_num_list = []

    def getData(self):
        while True:
            people_num = random.randint(0, 10)
            # cars_num = random.randint(0, 10)
            # motors_num = random.randint(0, 15)

            print(people_num)

            self.people_num_list.append(people_num)
            if len(self.people_num_list) > 30:
                self.people_num_list.pop(0)
            # self.cars_num_list.append(cars_num)
            # self.motors_num_list.append(motors_num)
            time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    # terminal = Terminal()
    # terminal.resize(1000, 500)
    # terminal.center()
    # terminal.show()
    sys.exit(app.exec_())
