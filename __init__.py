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

### XOR
population = Population.Population(2, 1, 10)

### House prices
#population = Population.Population(5, 1, 4)

mainWindow.addPopulation(population)

mainWindow.setupLayout()

sys.exit(app.exec_())
