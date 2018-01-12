# http://doc.qt.io/qt-4.8/classes.html
import random

from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Point(QPoint):
    # Red 0 - 255
    r = 0

    # Green 0 - 255
    g = 0

    # Blue 0 - 255
    b = 0

    # Alpha 0 - 255
    a = 255

    def __init__(self, x, y):
        super(Point, self).__init__(x, y)

        self.a = random.uniform(1, 255)
        self.r = random.uniform(1, 255)
        self.g = random.uniform(1, 255)
        self.b = random.uniform(1, 255)

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color
