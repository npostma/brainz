from PyQt4.QtCore import Qt
from PyQt4.QtGui import *


# Dockable wrapper for panel
class Window(QMainWindow):
    # Instance of the internal panel
    dockablePanels = list()

    initialized = False

    def __init__(self):
        super(Window, self).__init__()
        self.dockablePanels = list()
        self.initialized = False

    def addDockablePanel(self, dockablePanel):
        if (self.initialized == True):
            raise ValueError("Already started")

        self.dockablePanels.append(dockablePanel)

    def setupLayout(self):
        for (i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.setupLayout()
            self.addDockWidget(Qt.LeftDockWidgetArea, dockablePanel)

        self.move(0, 0)
        self.resize(1600, 800)
        self.show()

        self.initialized = True

    def update(self):
        for (i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.update()
