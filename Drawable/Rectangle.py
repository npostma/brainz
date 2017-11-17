# http://doc.qt.io/qt-4.8/classes.html

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Rectangle(QRect):
    r = 0

    g = 0

    b = 0

    a = 255

    def __init__(self, x, y, w, h):
        super(Rectangle, self).__init__(x, y, w, h)

        self.a = 255
        self.r = 0
        self.g = 0
        self.b = 0

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color
