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

    def update(self):
        for (i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.update()