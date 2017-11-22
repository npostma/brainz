import sys
from MRI import Panel
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# Main window
class Window(QMainWindow):
    # Instance of the internal panels
    panels = list()

    initialized = False

    activePopulation = None

    mainApplication = None

    mdi = None

    def __init__(self, mainApplication):
        super(Window, self).__init__()
        self.panels = list()
        self.initialized = False
        self.activePopulation = None
        self.mainApplication = mainApplication

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)



    def addPanel(self, subWindow):
        self.panels.append(subWindow)

        self.mdi.addSubWindow(subWindow)
        subWindow.show()
        subWindow.setupLayout()



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

        cascadePanels = QAction("&Cascade", self)
        cascadePanels.setShortcut("Ctrl+1")
        cascadePanels.setStatusTip('Cascade all panels')
        cascadePanels.triggered.connect(self.cascadePanels)

        tilePanels = QAction("&Tile", self)
        tilePanels.setShortcut("Ctrl+2")
        tilePanels.setStatusTip('Tile all panels')
        tilePanels.triggered.connect(self.tilePanels)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(closeApplication)

        fileMenu = mainMenu.addMenu('&Population')
        fileMenu.addAction(breedPopulation)
        fileMenu.addAction(teachPopulation)

        fileMenu = mainMenu.addMenu('&Windows')
        fileMenu.addAction(cascadePanels)
        fileMenu.addAction(tilePanels)

        self.setWindowState(Qt.WindowFullScreen)

        self.setWindowTitle("Taking over the world is the new hello world *EvIl LaUgHteR")

        self.move(0, 0)
        self.show()

        self.initialized = True

    def cascadePanels(self):
        self.mdi.cascadeSubWindows()

    def tilePanels(self):
        self.mdi.tileSubWindows()

    def teachPopulation(self):

        for (index) in range(0, 500):
            self.activePopulation.learn([-1, -1], [0])
            self.activePopulation.learn([1, -1], [1])
            self.activePopulation.learn([-1, 1], [1])
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
            panel = Panel.Panel(brain)
            self.addPanel(panel);
            self.update();

    def update(self):
        for (i, panel) in enumerate(self.panels):
            panel.update()
