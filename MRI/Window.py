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

    mainApplication = None

    def __init__(self, mainApplication):
        super(Window, self).__init__()
        self.dockablePanels = list()
        self.initialized = False
        self.activePopulation = None
        self.mainApplication = mainApplication

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
        breedPopulation.setShortcut("Ctrl+B")
        breedPopulation.setStatusTip('Crossover the networks in the current active population')
        # Todo: make some cool interface for this.
        breedPopulation.triggered.connect(self.breedPopulation)

        teachPopulation = QAction("&Learn some ...", self)
        teachPopulation.setShortcut("Ctrl+L")
        teachPopulation.setStatusTip('Do some more learning iterations for the current population')
        # Todo: make some cool interface for this.
        teachPopulation.triggered.connect(self.teachPopulation)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(closeApplication)

        fileMenu = mainMenu.addMenu('&Population')
        fileMenu.addAction(breedPopulation)
        fileMenu.addAction(teachPopulation)

        self.setWindowState(Qt.WindowFullScreen)

        self.setWindowTitle("Taking over the world is the new hello world *EvIl LaUgHteR")

        self.move(0, 0)
        self.show()

        self.initialized = True

    def teachPopulation(self):

        for (index) in range(0, 500):
            self.activePopulation.learn([0, 0], [0])
            self.activePopulation.learn([1, 0], [1])
            self.activePopulation.learn([0, 1], [1])
            self.activePopulation.learn([1, 1], [0])

            self.update()

            # Prevent main application from freezing!
            self.mainApplication.processEvents()

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
