import sys
from MRI import PanelDock
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# Dockable wrapper for panel
class Window(QMainWindow):
    # Instance of the internal panel
    dockablePanels = list()

    initialized = False

    activePopulation = None

    def __init__(self):
        super(Window, self).__init__()
        self.dockablePanels = list()
        self.initialized = False
        self.activePopulation = None

    def addDockablePanel(self, dockablePanel):
        self.dockablePanels.append(dockablePanel)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockablePanel)
        dockablePanel.setupLayout()

    def setupLayout(self):
        if (self.initialized == True):
            raise StandardError("Already started")

        closeApplication = QAction("&Close", self)
        closeApplication.setShortcut("Ctrl+Q")
        closeApplication.setStatusTip('Leave The App')
        closeApplication.triggered.connect(self.closeApplication)

        breedPopulation = QAction("&Breed!!!", self)
        breedPopulation.setShortcut("Ctrl+Q")
        breedPopulation.setStatusTip('Leave The App')
        # Todo: make some cool interface for this.
        breedPopulation.triggered.connect(self.breedPopulation)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(closeApplication)

        fileMenu = mainMenu.addMenu('&Population')
        fileMenu.addAction(breedPopulation)

        self.setWindowState(Qt.WindowFullScreen)

        self.move(0, 0)
        self.show()

        self.initialized = True

    def breedPopulation(self):
        newPopulation = self.activePopulation.breed()
        self.setPopulation(newPopulation)

    def closeApplication(self):
        sys.exit()

    def setPopulation(self, population):
        self.activePopulation = population
        for (i, brain) in enumerate(population.brains):
            panelDock = PanelDock.PanelDock(brain)
            self.addDockablePanel(panelDock);
            self.update();

    def update(self):
        for (i, dockablePanel) in enumerate(self.dockablePanels):
            dockablePanel.update()
