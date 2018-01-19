import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from MRI import Window
from AI import  Population

sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
#  excepthook override. Otherwise PyQT5 exceptions wont show
sys.excepthook = exception_hook


app = QtWidgets.QApplication(sys.argv)

mainWindow = Window.Window(app)

mainWindow.startListening()

population = Population.Population(2, 1, 5)

mainWindow.addPopulation(population)

mainWindow.setupLayout()

sys.exit(app.exec_())