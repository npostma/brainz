from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from AI import Neuron, Layer


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
        activationFunctionFormGrid = QFormLayout()
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
            learnFormGrid.addRow(QLabel("Input " + str(i) + ":"), decimalInput)

        for (i) in range(0, self.numOutputs):
            decimalInput = QLineEdit()
            self.learnOutputs.append(decimalInput)
            learnFormGrid.addRow(QLabel("Output " + str(i) + ":"), decimalInput)

        self.iterationsTextbox = QLineEdit()
        self.iterationsTextbox.setValidator(QIntValidator(0, 99999))
        self.iterationsTextbox.setText("500")
        learnFormGrid.addRow(QLabel("Num. of iterations:"), self.iterationsTextbox)

        applyActivationFunction = QPushButton()
        applyActivationFunction.clicked.connect(self.applyActivationClicked)
        applyActivationFunction.setText("Change function")

        compute = QPushButton()
        compute.clicked.connect(self.computeClicked)
        compute.setText("Compute")

        breed = QPushButton()
        breed.clicked.connect(self.breedClicked)
        breed.setText("Breed")

        teach = QPushButton()
        teach.clicked.connect(self.learnClicked)
        teach.setText("Learn")

        clone = QPushButton()
        clone.clicked.connect(self.cloneClicked)
        clone.setText("Clone")

        destroy = QPushButton()
        destroy.clicked.connect(self.destroyClicked)
        destroy.setText("Destroy")

        Show = QPushButton()
        Show.clicked.connect(self.showClicked)
        Show.setText("Show")

        hide = QPushButton()
        hide.clicked.connect(self.hideClicked)
        hide.setText("Hide")

        verticalStack.addLayout(computeFormGrid)
        verticalStack.addWidget(compute)

        verticalStack.addLayout(learnFormGrid)
        verticalStack.addWidget(teach)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        verticalStack.addWidget(line)

        verticalStack.addWidget(breed)
        verticalStack.addWidget(clone)
        verticalStack.addWidget(Show)
        verticalStack.addWidget(hide)
        verticalStack.addWidget(destroy)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        verticalStack.addWidget(line)

        self.layerTypeSelect = QComboBox()
        self.layerTypeSelect.addItem(Layer.Layer.TYPE_HIDDEN)
        self.layerTypeSelect.addItem(Layer.Layer.TYPE_OUTPUT)
        activationFunctionFormGrid.addRow(QLabel("LType:"), self.layerTypeSelect)

        self.activationFunctionSelect = QComboBox()
        self.activationFunctionSelect.addItem(Neuron.Neuron.ACTIVATION_SIGMOID)
        self.activationFunctionSelect.addItem(Neuron.Neuron.ACTIVATION_RELU)
        self.activationFunctionSelect.addItem(Neuron.Neuron.ACTIVATION_TANH)
        self.activationFunctionSelect.addItem(Neuron.Neuron.ACTIVATION_THRESHOLD)
        activationFunctionFormGrid.addRow(QLabel("AFunction:"), self.activationFunctionSelect)

        verticalStack.addLayout(activationFunctionFormGrid)

        verticalStack.addWidget(applyActivationFunction)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)

        verticalStack.addWidget(line)

        verticalStack.addStretch()

        self.setLayout(verticalStack)

    def applyActivationClicked(self):
        self.mainWindow.activePopulation.setActivationFunction(str(self.layerTypeSelect.currentText()), str(self.activationFunctionSelect.currentText()))
        self.mainWindow.update()

    def computeClicked(self):
        if self.mainWindow.activePopulation is None:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 5000)
            return

        data = list()
        for (i, inputField) in enumerate(self.computeInputs):
            if not inputField.text():
                self.mainWindow.windowStatusBar.showMessage('Missing compute data', 5000)
                return

            data.append(float(inputField.text()))

        self.mainWindow.activePopulation.compute(data)
        self.mainWindow.update()

    def showClicked(self):
        index = self.populationSelection.currentIndex()

        if len(self.mainWindow.panels) <= index or index < 0:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 5000)
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
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 5000)
            return

            # Remove panels from te list
        brainPanels = self.mainWindow.panels[index]

        # Clean up panels
        for (i, panelData) in enumerate(brainPanels):
            window = panelData['window']
            window.hide()

    def breedClicked(self):
        self.mainWindow.breedPopulation()

    def cloneClicked(self):
        self.mainWindow.clonePopulation()

    def learnClicked(self):
        if self.mainWindow.activePopulation is None:
            self.mainWindow.windowStatusBar.showMessage('No active populations left. Please reboot the program', 5000)
            return

        inputData = list()
        inputData.append(list())
        numInSet = 0
        for (i, inputField) in enumerate(self.learnInputs):
            trainingSet = inputField.text()

            if ';' in trainingSet:
                trainingSet = trainingSet.split(';')

                for (j, value) in enumerate(trainingSet):
                    if i == 0:
                        numInSet += 1
                    elif numInSet != len(trainingSet):
                        self.mainWindow.windowStatusBar.showMessage('Input of data set is not correct, sizes do not match'
                                                                    , 5000)
                        return

                    if j >= len(inputData):
                        inputData.insert(j, list())

                    if not value:
                        self.mainWindow.windowStatusBar.showMessage('Input data of dataset is not correct', 5000)
                        return

                    inputData[j].append(float(value))
            else:
                if i == 0:
                    numInSet = 1
                elif numInSet != 1:
                    self.mainWindow.windowStatusBar.showMessage('Input of dataset is not correct, sizes do not match',
                                                                5000)
                    return

                if not trainingSet:
                    self.mainWindow.windowStatusBar.showMessage('Input data of dataset is not correct', 5000)
                    return

                inputData[0].append(float(trainingSet))

        expectedOutput = list()
        expectedOutput.append(list())
        for (i, outputField) in enumerate(self.learnOutputs):
            outputSet = outputField.text()

            if ';' in outputSet:
                outputSet = outputSet.split(';')

                for (j, value) in enumerate(outputSet[:-1]):

                    if j >= len(expectedOutput):
                        expectedOutput.insert(j, list())

                    expectedOutput[j].append(float(value))
            else:
                if not outputSet:
                    self.mainWindow.windowStatusBar.showMessage('Output data of data set is not correct', 5000)
                    return
                expectedOutput[0].append(float(outputSet))

        numberOfIterations = int(self.iterationsTextbox.text())

        # Check if inputs are matching up
        for (setNr, trainingSet) in enumerate(inputData):
            try:
                self.mainWindow.teachPopulation(trainingSet, expectedOutput[setNr], numberOfIterations)
            except IndexError:
                self.mainWindow.windowStatusBar.showMessage('Output of data set is not correct, Not matching input',
                                                            5000)

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
