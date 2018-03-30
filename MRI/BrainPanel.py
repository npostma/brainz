from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Drawable import Rectangle, Point, Line, Label
from Drawable.Calculator import Metrics

# Convert brain into a set of drawable objects
from MRI import Canvas


class BrainPanel(QWidget):
    # Instance of the brain to scan
    brain = None

    # keep track of the location of a neuron (for drawing lines)
    points = list()

    rectangles = list()

    lines = list()

    neuronValueStrings = list()

    inputs = list()

    functionNames = list()

    canvas = None

    drawingMaxWidth = 0

    drawingMaxHeight = 0

    canvasTool = None

    def __init__(self, brain):
        super(BrainPanel, self).__init__()

        self.brain = brain
        self.canvas = Canvas.Canvas()
        self.inputs = list()
        self.functionNames = list()

        # Static drawable objects
        self.rectangles = list()
        self.points = list()

        # Dynamic drawable objects
        self.lines = list()
        self.neuronValueStrings = list()
        self.brainStrings = list()

        self.drawingMaxWidth = 0
        self.drawingMaxHeight = 0

        self.canvasTool = Metrics.Metrics()

        self.createStaticDrawables()

    def close(self):
        self.brain = None
        self.points = None
        self.rectangles = None
        self.lines = None
        self.inputs = None
        self.canvas = None
        self.drawingMaxWidth = None
        self.drawingMaxHeight = None
        return super(BrainPanel, self).close()

    def setupLayout(self):
        formGrid = QGridLayout()

        submit = QPushButton()
        submit.clicked.connect(self.SubmitClicked)
        submit.setText("Compute")

        lastIndex = 0
        for (i) in range(0, (self.brain.inputSize - self.brain.biasSize)):
            decimalInput = QLineEdit()
            self.inputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            formGrid.addWidget(decimalInput, 1, i)
            lastIndex = i

        lastIndex += 1

        formGrid.addWidget(submit, 1, lastIndex)

        formGrid.addWidget(self.canvas, 0, 0, 1, lastIndex + 1)

        self.resize(self.canvasTool.getTotalWidth(self.brain), self.canvasTool.getTotalHeight(self.brain))
        self.parentWidget().resize(self.canvasTool.getTotalWidth(self.brain), self.canvasTool.getTotalHeight(self.brain))

        self.setLayout(formGrid)

    def SubmitClicked(self):
        data = list()
        for (i, inputField) in enumerate(self.inputs):
            try:
                data.append(float(inputField.text()))
            except ValueError:
                self.setWindowTitle('Value not correct')
                return

        self.brain.compute(data)
        self.update()

    def update(self):
        self.updateDynamicDrawables()

        self.brain.measureOverallFitness();
        self.setWindowTitle("OverallF: "
                            + str(round(self.brain.overallFitness, 5))
                            + " LastF: "
                            + str(round(self.brain.fitness, 5))
                            + " Cycle:" + str(self.brain.learnCycle))

        self.canvas.reset()

        self.canvas.addStrings(self.getStrings())
        self.canvas.addLines(self.getLines())

        self.canvas.repaint()

    def getRectangles(self):
        return self.rectangles

    def getLines(self):
        lines = list()
        for (x, lineListX) in enumerate(self.lines):
            for (y, lineListY) in enumerate(lineListX):
                for (z, line) in enumerate(lineListY):
                    lines.append(line)
        return lines

    def getStrings(self):
        strings = list()

        for (x, stringList) in enumerate(self.neuronValueStrings):
            for (y, string) in enumerate(stringList):
                strings.append(string)

        for (x, functionName) in enumerate(self.functionNames):
            strings.append(functionName)

        return strings

    def updateDynamicDrawables(self):
        self.updateStrings()
        self.updateLines()

    def createStaticDrawables(self):
        self.createRectangles()
        self.createLines()
        self.createStrings()

        self.canvas.addRectangles(self.rectangles)

    def updateStrings(self):
        for (layerNr, layer) in enumerate(self.brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                self.neuronValueStrings[layerNr][neuronNr].setText(str(neuron.value))

    def createStrings(self):
        self.functionNames = list()

        for (layerNr, layer) in enumerate(self.brain.layers):

            if layerNr >= len(self.neuronValueStrings):
                self.neuronValueStrings.insert(layerNr, list())

            for (neuronNr, neuron) in enumerate(layer.neurons):
                centerPoint = self.points[layerNr][neuronNr] - Point.Point(20, 12)

                self.neuronValueStrings[layerNr].insert(neuronNr, Label.Label(centerPoint, str(neuron.value)))

                functionNamePoint = centerPoint + Point.Point(0, 30)

                # Input layers do not use the activation function. Therefore hide the label
                if layerNr != 0:
                    self.functionNames.append(Label.Label(functionNamePoint, str(neuron.activeActivationName)))

    def createRectangles(self):
        for (layerNr, layer) in enumerate(self.brain.layers):

            topLeftLayerPoint = self.canvasTool.getLayerTopLeft(layer)
            bottomRightLayerPoint = self.canvasTool.getLayerBottomRight(layer)

            rect = Rectangle.Rectangle(topLeftLayerPoint, bottomRightLayerPoint)

            if layerNr >= len(self.points):
                self.points.insert(layerNr, list())

            self.rectangles.append(rect)

            for (neuronNr, neuron) in enumerate(layer.neurons):
                centerPoint = self.canvasTool.getNeuronCenter(neuron)
                topLeftPoint = self.canvasTool.getNeuronTopLeft(neuron)
                bottomRightPoint = self.canvasTool.getNeuronBottomRight(neuron)

                self.points[layerNr].insert(neuronNr, centerPoint)

                rect = Rectangle.Rectangle(topLeftPoint, bottomRightPoint)

                # Color bias neurons orange
                if neuron.type == neuron.TYPE_BIAS:
                    rect.colorOrange()

                self.rectangles.append(rect)

    def createLines(self):
        for (layerNr, layer) in enumerate(self.brain.layers):

            if layerNr >= len(self.lines):
                self.lines.insert(layerNr, list())

            for (neuronNr, neuron) in enumerate(layer.neurons):

                if neuronNr >= len(self.lines[layerNr]):
                    self.lines[layerNr].insert(neuronNr, list())

                for (synapseNr, synapse) in enumerate(neuron.synapses):
                    startPoint = self.canvasTool.getNeuronRightAnchor(synapse.leftNeuron)
                    endPoint = self.canvasTool.getNeuronLeftAnchor(synapse.rightNeuron)

                    line = Line.Line(startPoint, endPoint)
                    line.setWeight(synapse.weight)

                    self.lines[layerNr][neuronNr].insert(synapseNr, line)

    def updateLines(self):
        for (layerNr, layer) in enumerate(self.brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                for (synapseNr, synapse) in enumerate(neuron.synapses):
                    self.lines[layerNr][neuronNr][synapseNr].setWeight(synapse.weight)
