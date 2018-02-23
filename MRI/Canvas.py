# http://doc.qt.io/qt-4.8/classes.html
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math, random, sys

from Drawable import Point


class Canvas(QWidget):
    points = list()

    rectangles = list()

    lines = list()

    strings = list()

    heightMap = {}

    def __init__(self):
        super(Canvas, self).__init__()

        self.resetAll()

    def resetAll(self):
        self.rectangles = list()
        self.points = list()
        self.lines = list()
        self.strings = list()
        self.heightMap = {}

    def reset(self):
        self.lines = list()
        self.strings = list()

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

    def addRectangle(self, rect):
        self.rectangles.append(rect)

    def addLine(self, line):
        self.lines.append(line)

    def addString(self, string):
        self.strings.append(string)

    def addRectanges(self, rectangles):
        for (i, rectangle) in enumerate(rectangles):
            self.addRectangle(rectangle)

    def addLines(self, lines):
        for (i, line) in enumerate(lines):
            self.addLine(line)

    def addStrings(self, strings):
        for (i, string) in enumerate(strings):
            self.addString(string)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        for (pointNr, point) in enumerate(self.points):
            self.drawPoint(painter, point)

        for (rectNr, rect) in enumerate(self.rectangles):
            self.drawRect(painter, rect)

        for (lineNr, line) in enumerate(self.lines):
            self.drawLine(painter, line)

        for (stringNr, string) in enumerate(self.strings):
            self.drawString(painter, string)

        painter.end()

    def drawPoint(self, painter, point):
        painter.setPen(point.getColor())
        painter.drawPoint(point)

    def drawRect(self, painter, rect):
        painter.setPen(rect.getColor())
        painter.drawRect(rect)

    def drawLine(self, painter, line):
        painter.setPen(line.getPen())
        painter.drawLine(line)

    def drawString(self, painter, string):
        painter.setPen(string.getPen())
        painter.drawText(string.getX(), string.getY(), string.getText())
