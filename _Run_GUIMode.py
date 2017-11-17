import sys
from PyQt4 import QtGui

from MRI import Window
from AI import  Population

app = QtGui.QApplication(sys.argv)

mainWindow = Window.Window()

population = Population.Population(2, 1, 5)

mainWindow.setPopulation(population)



mainWindow.setupLayout();

for (index) in range(0, 500):
    population.learn([0, 0], [0])
    population.learn([1, 0], [1])
    population.learn([0, 1], [1])
    population.learn([1, 1], [0])

    mainWindow.update()


    # Prevent main application from freezing!
    app.processEvents()

    # time.sleep(0.01)

mainWindow.update()

sys.exit(app.exec_())
