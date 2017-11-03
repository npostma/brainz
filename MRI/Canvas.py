#http://doc.qt.io/qt-4.8/classes.html
from PyQt4.QtGui import *

from Drawable import Point


class Canvas(QWidget):

    points = list;

    rects = list;

    heightMap = {};

    def __init__(self):
        super(Canvas, self).__init__()

        self.points = list()

        self.show()

    def registerY(self, x):
        if x in self.heightMap:
            self.heightMap[x] += 1
        else:
            self.heightMap[x] = 1

    def addXPoint(self, x=int):
        self.registerY(x)
        point = Point.Point(x, self.heightMap[x])
        self.addPoint(point)

    def addPoint(self, point=Point):
        self.points.append(point)

    def addRect(self, rect):
        self.rects.append(rect)

    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)
        for (pointNr, point) in enumerate(self.points):
            self.drawPoint(painter, point)

        for (rectNr, rect) in enumerate(self.rects):
            self.drawRect(painter, rect)

        painter.end()

    def drawPoint(self, painter, point):
        painter.setPen(point.getColor())

        painter.drawPoint(point)

    def drawRect(self, painter, rect):
        painter.setPen(rect.getColor())

        painter.drawRect(rect)
