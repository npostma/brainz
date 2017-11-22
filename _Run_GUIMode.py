import sys
from PyQt4 import QtGui

from MRI import Window
from AI import  Population

app = QtGui.QApplication(sys.argv)

mainWindow = Window.Window(app)

mainWindow.startListening()

population = Population.Population(2, 1, 5)

mainWindow.addPopulation(population)

mainWindow.setupLayout()

mainWindow.teachPopulation()

sys.exit(app.exec_())
