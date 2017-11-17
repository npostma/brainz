import sys
from PyQt4 import QtGui

from MRI import PanelDock, Window
from AI import Brain

brain = Brain.Brain(2, 1)
app = QtGui.QApplication(sys.argv)
panelDock = PanelDock.PanelDock(brain)
mainWindow = Window.Window(panelDock)

for (index) in range(0, 5000):
    brain.learn([0, 0], [0])
    brain.learn([1, 0], [1])
    brain.learn([0, 1], [1])
    brain.learn([1, 1], [0])

    mainWindow.update()


    # Prevent main application from freezing!
    app.processEvents()

    # time.sleep(0.01)

mainWindow.update()

sys.exit(app.exec_())
