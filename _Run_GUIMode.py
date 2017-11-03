import sys
from PyQt4 import QtGui, QtCore
from MRI import GUI, Canvas
from AI import Brain

brain = Brain.Brain()
app = QtGui.QApplication(sys.argv)

gui = GUI.GUI(brain)
gui.convertToDrawables()

canvas = Canvas.Canvas()
canvas.addRectanges(gui.getRectangles())


sys.exit(app.exec_())