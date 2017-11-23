from PyQt4.QtGui import *


class PopulationPanel(QWidget):
    computeInputs = list()

    learnInputs = list()

    learnOutputs = list()

    iterationsTextbox = None

    numInputs = 0

    numOutputs = 0

    mainWindow = None

    populationSelection = None

    def __init__(self, mainWindow, numInputs, numOutputs):
        super(PopulationPanel, self).__init__()

        self.mainWindow = mainWindow
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.computeInputs = list()
        self.learnInputs = list()
        self.learnOutputs = list()
        self.iterationsTextbox = None
        self.populationSelection = None

    def setupLayout(self):
        verticalStack = QVBoxLayout()
        computeFormGrid = QFormLayout()
        learnFormGrid = QFormLayout()

        self.populationSelection = QComboBox()
        computeFormGrid.addRow(QLabel("Active population:"), self.populationSelection)

        for (i) in range(0, self.numInputs):
            decimalInput = QLineEdit()
            self.computeInputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            computeFormGrid.addRow(QLabel("Input " + str(i) + ":"), decimalInput)
            decimalInput = QLineEdit()
            self.learnInputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            learnFormGrid.addRow(QLabel("Input " + str(i) + ":"), decimalInput)

        for (i) in range(0, self.numOutputs):
            decimalInput = QLineEdit()
            self.learnOutputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            learnFormGrid.addRow(QLabel("Output " + str(i) + ":"), decimalInput)

        self.iterationsTextbox = QLineEdit()
        self.iterationsTextbox.setValidator(QDoubleValidator(0.99, 9.99, 2))
        self.iterationsTextbox.setText("500")
        learnFormGrid.addRow(QLabel("Num. of iterations:"), self.iterationsTextbox)

        submit = QPushButton()
        submit.clicked.connect(self.computeClicked)
        submit.setText("Compute")

        breed = QPushButton()
        breed.clicked.connect(self.breedClicked)
        breed.setText("Breed")

        teach = QPushButton()
        teach.clicked.connect(self.learnClicked)
        teach.setText("Learn")

        destroy = QPushButton()
        destroy.clicked.connect(self.destroyClicked)
        destroy.setText("Destroy")

        Show = QPushButton()
        Show.clicked.connect(self.showClicked)
        Show.setText("Show")

        Hide = QPushButton()
        Hide.clicked.connect(self.hideClicked)
        Hide.setText("Hide")

        verticalStack.addLayout(computeFormGrid)
        verticalStack.addWidget(submit)

        verticalStack.addLayout(learnFormGrid)
        verticalStack.addWidget(teach)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)

        verticalStack.addWidget(line)
        verticalStack.addWidget(breed)
        verticalStack.addWidget(Show)
        verticalStack.addWidget(Hide)
        verticalStack.addWidget(destroy)

        verticalStack.addStretch()

        self.setLayout(verticalStack)

    def computeClicked(self):
        if self.mainWindow.activePopulation is None:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 2000)
            return

        data = list()
        for (i, inputField) in enumerate(self.computeInputs):
            data.append(float(inputField.text()))

        self.mainWindow.activePopulation.compute(data)
        self.mainWindow.update()

    def showClicked(self):
        index = self.populationSelection.currentIndex()

        if len(self.mainWindow.panels) <= index or index < 0:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 2000)
            return

            # Remove panels from te list
        brainPanels = self.mainWindow.panels[index]

        # Clean up panels
        for (i, panelData) in enumerate(brainPanels):
            window = panelData['window']
            window.show()

    def hideClicked(self):
        index = self.populationSelection.currentIndex()

        if len(self.mainWindow.panels) <= index or index < 0:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 2000)
            return

            # Remove panels from te list
        brainPanels = self.mainWindow.panels[index]

        # Clean up panels
        for (i, panelData) in enumerate(brainPanels):
            window = panelData['window']
            window.hide()

    def breedClicked(self):
        self.mainWindow.breedPopulation()

    def learnClicked(self):
        if self.mainWindow.activePopulation is None:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 2000)
            return

        inputData = list()
        for (i, inputField) in enumerate(self.learnInputs):
            inputData.append(float(inputField.text()))

        expectedOutput = list()
        for (i, outputField) in enumerate(self.learnOutputs):
            expectedOutput.append(float(outputField.text()))

        numberOfIterations = int(self.iterationsTextbox.text())
        self.mainWindow.teachPopulation(inputData, expectedOutput, numberOfIterations)

    def destroyClicked(self):
        self.mainWindow.destroyPopulation(self.populationSelection.currentIndex())

    def updatePopulationList(self):
        self.populationSelection.clear()
        for (populationNr, population) in enumerate(self.mainWindow.populations):
            self.populationSelection.addItem(str(populationNr))

        self.populationSelection.activated[str].connect(self.activatePopulation)

        # Selecting active index
        try:
            self.populationSelection.setCurrentIndex(
                self.mainWindow.populations.index(self.mainWindow.activePopulation))
        except ValueError as err:
            self.populationSelection.setCurrentIndex(0)

        self.show()

    def activatePopulation(self, option):
        self.mainWindow.activePopulation = self.mainWindow.populations[int(option)]
