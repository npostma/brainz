import sys
import time
import sip

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from MRI import BrainPanel, PopulationPanel


# Main window
class Window(QMainWindow):
    # Populations
    populations = list()

    # Instances of the internal panels
    panels = list()

    initialized = False

    activePopulation = None

    mainApplication = None

    mdi = None

    leftDock = None

    populationPanel = None

    # Timed loop variables
    startTime = 0
    endTime = 0
    deltaTime = 0

    def __init__(self, mainApplication):
        super(Window, self).__init__()
        self.panels = list()
        self.initialized = False
        self.activePopulation = None
        self.mainApplication = mainApplication

        # Timed loop variables
        self.startTime = 0
        self.endTime = 0
        self.deltaTime = 0

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

    def addPanel(self, panel, populationNr):

        if (populationNr >= len(self.panels)):
            self.panels.insert(populationNr, list())

        subWindow = self.mdi.addSubWindow(panel)

        self.panels[populationNr].append({'panel': panel, 'window': subWindow})

        panel.show()
        panel.setupLayout()

    def setupLayout(self):
        if (self.initialized == True):
            raise StandardError("Already started")

        self.leftDock = QDockWidget("Population control", self)
        self.populationPanel = PopulationPanel.PopulationPanel(self, self.activePopulation.inputSize)
        self.populationPanel.setupLayout()
        self.leftDock.setWidget(self.populationPanel)
        self.leftDock.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)

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

        self.populationPanel.updatePopulationList()

        self.setWindowTitle("Taking over the world is the new hello world *EvIl LaUgHteR")

        self.move(0, 0)
        self.show()

        self.initialized = True


    def cascadePanels(self):
        self.mdi.cascadeSubWindows()

    def tilePanels(self):
        self.mdi.tileSubWindows()

    def timedUpdate(self):

        if self.startTime == 0:
            self.startTime = time.time()

        self.endTime = time.time()

        self.deltaTime = self.endTime - self.startTime

        if self.deltaTime < 0.1:
            return

        # restart the mesuring of time
        self.startTime = time.time()

        # Do an update of the windows every 100ms.
        # 1 - Faster is not readable and so, it has no function
        # 2 - More updates slow down the learning process significantly
        start_time = time.time()
        end_time = time.time()

        # cProfile.runctx('self.update()',globals(),locals())
        self.update()

    def teachPopulation(self):
        if (self.activePopulation == None):
            # todo: message in to statusbar
            return;

        for (index) in range(0, 500):
            # cProfile.runctx('self.activePopulation.learn([0, 0], [0])',globals(),locals())
            self.activePopulation.learn([0, 0], [0])
            self.timedUpdate()
            self.activePopulation.learn([1, 0], [1])
            self.timedUpdate()
            self.activePopulation.learn([0, 1], [1])
            self.timedUpdate()
            self.activePopulation.learn([1, 1], [0])
            self.timedUpdate()
            # Prevent main application from freezing!
            #self.mainApplication.processEvents()

    def breedPopulation(self):
        if(self.activePopulation == None):
            #todo: message in to statusbar
            return;

        newPopulation = self.activePopulation.breed()
        self.addPopulation(newPopulation)

    def destroyPopulation(self, index):

        if(len(self.panels) <= index or index < 0):
            # todo: message in to statusbar
            return

        # Remove panels from te list
        brainPanels = self.panels.pop(index)

        # Clean up panels
        for (i, panelData) in enumerate(brainPanels):
            window = panelData['window']
            panel = panelData['panel']
            panel.close()
            # Delete panel from the container
            self.mdi.removeSubWindow(panel)
            # Delete contents
            panel.deleteLater()
            panel.setParent(None)
            sip.delete(panel)

            window.close()

        # remove population from the list
        populationToDestoy = self.populations.pop(index)

        if(self.activePopulation == populationToDestoy):
            self.activePopulation = next(iter(self.populations or []), None)

        # Update te population selection list
        self.populationPanel.updatePopulationList()

    def closeApplication(self):
        sys.exit()

    def addPopulation(self, population):
        self.populations.append(population)

        self.activePopulation = population
        for (i, brain) in enumerate(population.brains):
            panel = BrainPanel.BrainPanel(brain)
            self.addPanel(panel, len(self.populations) - 1)
            self.update()

        if(self.populationPanel != None):
            self.populationPanel.updatePopulationList()

    def update(self):
        for (i, panelGroupList) in enumerate(self.panels):
            for (i, panelData) in enumerate(panelGroupList):
                panelData['panel'].update()
