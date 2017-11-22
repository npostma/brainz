import sys
from PyQt4 import QtGui

from MRI import Window
from AI import  Population

app = QtGui.QApplication(sys.argv)

mainWindow = Window.Window(app)

population = Population.Population(2, 1, 5)

mainWindow.setupLayout()

mainWindow.setPopulation(population)


mainWindow.teachPopulation()

sys.exit(app.exec_())
