from PyQt4.QtCore import Qt
from PyQt4.QtGui import *

# Dockable wrapper for panel
class Window(QMainWindow):
    # Instance of the internal panel
    dockablePanels = []

    def __init__(self, defaultDockablePanel):
        super(Window, self).__init__()

        self.dockablePanels.append(defaultDockablePanel)

        self.setupLayout()

    def setupLayout(self):
        for(i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.setupLayout()
            self.addDockWidget(Qt.LeftDockWidgetArea  , dockablePanel)

        self.move(0, 0)
        self.resize(1600, 800)
        self.show()

    def update(self):
        for (i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.update()