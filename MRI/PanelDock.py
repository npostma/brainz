from PyQt4.QtGui import *
from MRI import Panel

# Dockable wrapper for panel
class PanelDock(QDockWidget):
    # Instance of the internal panel
    panel = None

    def __init__(self, brain):
        super(PanelDock, self).__init__()

        self.panel = Panel.Panel(brain)

        self.setupLayout()

    def setupLayout(self):
        self.panel.setupLayout()

    def update(self):
        self.panel.update()