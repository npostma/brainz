from PyQt4.QtGui import *



class PopulationPanel(QWidget):
    inputs = list()

    numInputs = 0

    mainWindow = None

    populationSelection = None

    def __init__(self, mainWindow, numInputs):
        super(PopulationPanel, self).__init__()

        self.mainWindow = mainWindow
        self.numInputs = numInputs
        self.inputs = list()

    def setupLayout(self):
        formGrid = QVBoxLayout()

        self.populationSelection = QComboBox()
        formGrid.addWidget(self.populationSelection)

        submit = QPushButton()
        submit.clicked.connect(self.computeClicked)
        submit.setText("Compute")

        lastIndex = 0
        for (i) in range(0, self.numInputs):
            decimalInput = QLineEdit()
            self.inputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            formGrid.addWidget(decimalInput)
            lastIndex = i

        lastIndex += 1

        breed = QPushButton()
        breed.clicked.connect(self.breedClicked)
        breed.setText("Breed")

        teach = QPushButton()
        teach.clicked.connect(self.learnClicked)
        teach.setText("Learn")

        destroy = QPushButton()
        destroy.clicked.connect(self.destroyClicked)
        destroy.setText("Destroy")

        formGrid.addWidget(submit)
        formGrid.addWidget(breed)
        formGrid.addWidget(teach)
        formGrid.addWidget(destroy)
        formGrid.addStretch()
        self.setLayout(formGrid)

    def computeClicked(self):
        if (self.mainWindow.activePopulation == None):
            # todo: message in to statusbar
            return;

        data = list()
        for (i, input) in enumerate(self.inputs):
            data.append(float(input.text()))

        self.mainWindow.activePopulation.compute(data)
        self.mainWindow.update()

    def breedClicked(self):
        self.mainWindow.breedPopulation()

    def learnClicked(self):
        self.mainWindow.teachPopulation()

    def destroyClicked(self):
        self.mainWindow.destroyPopulation(self.populationSelection.currentIndex())

    def updatePopulationList(self):
        self.populationSelection.clear()
        for (populationNr, population) in enumerate(self.mainWindow.populations):
            self.populationSelection.addItem(str(populationNr))

        self.populationSelection.activated[str].connect(self.activatePopulation)

        # Selecting active index
        try:
            self.populationSelection.setCurrentIndex(self.mainWindow.populations.index(self.mainWindow.activePopulation))
        except ValueError as err:
            self.populationSelection.setCurrentIndex(0)

        self.show()

    def activatePopulation(self, option):
        self.mainWindow.activePopulation = self.mainWindow.populations[int(option)]
