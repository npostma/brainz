# http://doc.qt.io/qt-4.8/classes.html

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Line(QLine):
    r = 0

    g = 0

    b = 0

    a = 255

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
        if (weight < 0):
            a = abs(weight) * 100
            r = abs(weight) * 100
            if (a > 255):
                a = 255
                r = 255

            self.width = 2
            self.g = 0
            self.r = r
            self.a = a
        else:

            r = 0
            g = weight * 100
            if (g > 255):
                g = 255

            self.width = (1 + weight) * 2
            self.g = g
            self.r = 9
            self.a = 255

    def getPen(self):
        pen = QPen(self.getColor())
        pen.setWidthF(self.width)
        return pen
