from PyQt4.QtGui import *
from MRI import Panel

# Dockable wrapper for panel
class PanelDock(QDockWidget):
    # Instance of the internal panel
    panel = None

    def __init__(self, brain):
        super(PanelDock, self).__init__()

        self.panel = Panel.Panel(brain)

    def setupLayout(self):
        self.panel.setupLayout()



        self.panel.move(0, 0)
        self.panel.resize(1600, 800)
        self.panel.show()

    def update(self):
        self.panel.update()