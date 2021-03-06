# http://doc.qt.io/qt-4.8/classes.html

from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Rectangle(QRect):
    # Red 0 - 255
    r = 0

    # Green 0 - 255
    g = 0

    # Blue 0 - 255
    b = 0

    # Alpha 0 - 255
    a = 255

    def __init__(self, topLeft, bottomRight):
        super(Rectangle, self).__init__(topLeft, bottomRight)

        self.a = 255
        self.r = 0
        self.g = 0
        self.b = 0

    def getColor(self):
        color = QColor(self.r, self.g, self.b, self.a)
        return color

    def colorOrange(self):
        self.r = 255
        self.g = 165
        self.b = 0
