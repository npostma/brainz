import sys
from PyQt4 import QtGui

from MRI import PanelDock, Window
from AI import Brain

brain = Brain.Brain(2, 1)
brain2 = Brain.Brain(2, 1)

app = QtGui.QApplication(sys.argv)
panelDock = PanelDock.PanelDock(brain)
panelDock2 = PanelDock.PanelDock(brain2)

mainWindow = Window.Window()

mainWindow.addDockablePanel(panelDock);
mainWindow.addDockablePanel(panelDock2);
mainWindow.setupLayout();

for (index) in range(0, 2500):
    brain.learn([0, 0], [0])
    brain.learn([1, 0], [1])
    brain.learn([0, 1], [1])
    brain.learn([1, 1], [0])

    brain2.learn([0, 0], [0])
    brain2.learn([1, 0], [1])
    brain2.learn([0, 1], [1])
    brain2.learn([1, 1], [0])


    mainWindow.update()


    # Prevent main application from freezing!
    app.processEvents()

    # time.sleep(0.01)

mainWindow.update()

sys.exit(app.exec_())
