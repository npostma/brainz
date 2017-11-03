import sys
from PyQt4 import QtGui, QtCore
from MRI import GUI, Canvas
from AI import Brain

brain = Brain.Brain()
app = QtGui.QApplication(sys.argv)

gui = GUI.GUI(brain)

canvas = Canvas.Canvas()


sys.exit(app.exec_())