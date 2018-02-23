# http://doc.qt.io/qt-4.8/classes.html

from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Line(QLine):
    # Red 0 - 255
    r = 0

    # Green 0 - 255
    g = 0

    # Blue 0 - 255
    b = 0

    # Alpha 0 - 255
    a = 255

    # Line width
    width = 1

    def __init__(self, a, b):
        super(Line, self).__init__(a, b)

        self.a = 255
        self.r = 0
        self.g = 0
        self.b = 0

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)

        return color

    def setWeight(self, weight):
        a = abs(weight) * 30
        c = abs(weight) * 50

        if a >= 200:
            a = 200

        if c >= 255:
            c = 255

        if weight < 0:
            self.g = 0
            self.r = c
        else:
            self.r = 0
            self.g = c

        self.a = 255 - a
        self.width = (abs(weight) * 2) + 1

    def getPen(self):
        pen = QPen(self.getColor())
        pen.setWidthF(self.width)
        return pen
