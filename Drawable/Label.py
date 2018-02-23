# http://doc.qt.io/qt-4.8/classes.html

from PyQt5.QtGui import *


class Label():
    # Red 0 - 255
    r = 0

    # Green 0 - 255
    g = 0

    # Blue  0 - 255
    b = 0

    # Alpha  0 - 255
    a = 255

    # Text width
    width = 1

    # Startpoint
    point = None

    def __init__(self, point, text):
        self.data = text
        self.point = point
        self.a = 255
        self.r = 0
        self.g = 0
        self.b = 0
        self.width = 1

    def getText(self):
        return str(self.data)

    def getPoint(self):
        return self.point

    def setText(self, text):
        self.data = text

    def getX(self):
        x = self.point.x()
        return x

    def getY(self):
        return self.point.y()

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color

    def getPen(self):
        pen = QPen(self.getColor())
        pen.setWidthF(self.width)
        return pen
