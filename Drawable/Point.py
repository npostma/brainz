# http://doc.qt.io/qt-4.8/classes.html
import random

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Point(QPoint):
    r = 0;

    g = 0;

    b = 0;

    a = 255;

    def __init__(self, x, y):
        super(Point, self).__init__(x, y)

        self.a = random.uniform(1, 255)
        self.r = random.uniform(1, 255)
        self.g = random.uniform(1, 255)
        self.b = random.uniform(1, 255)

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color
