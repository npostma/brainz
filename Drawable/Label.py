# http://doc.qt.io/qt-4.8/classes.html

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Label(QString):
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
        super(Label, self).__init__(QString.fromAscii(text))

        self.data = text
        self.point = point
        self.a = 255
        self.r = 0
        self.g = 0
        self.b = 0
        self.width = 1

    def getText(self):
        return self

    def getPoint(self):
        return self.point

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color

    def getPen(self):
        pen = QPen(self.getColor())
        pen.setWidthF(self.width)
        return pen
