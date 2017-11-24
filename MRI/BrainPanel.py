from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Drawable import Rectangle, Point, Line, Label

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

    def __init__(self, brain):
        super(BrainPanel, self).__init__()

        self.brain = brain
        self.canvas = Canvas.Canvas()
        self.inputs = list()
        self.functionNames = list()

        # Static drawables
        self.rectangles = list()
        self.points = list()

        # Dynmic drawables
        self.lines = list()
        self.neuronValueStrings = list()
        self.brainStrings = list()

        self.drawingMaxWidth = 0
        self.drawingMaxHeight = 0

        self.createStaticDrawables()

    def close(self):
        self.brain = None
        self.points = None
        self.rectangles = None
        self.lines = None
        self.strings = None
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
        for (i) in range(0, self.brain.inputSize):
            decimalInput = QLineEdit()
            self.inputs.append(decimalInput)
            decimalInput.setValidator(QDoubleValidator(0.99, 9.99, 2))
            formGrid.addWidget(decimalInput, 1, i)
            lastIndex = i

        lastIndex += 1

        formGrid.addWidget(submit, 1, lastIndex)

        formGrid.addWidget(self.canvas, 0, 0, 1, lastIndex + 1)

        self.resize(self.drawingMaxWidth + 100, self.drawingMaxHeight + 100)
        self.parentWidget().resize(self.drawingMaxWidth + 100, self.drawingMaxHeight + 100)

        self.setLayout(formGrid)

    def SubmitClicked(self):
        data = list()
        for (i, input) in enumerate(self.inputs):
            data.append(float(input.text()))

        self.brain.compute(data)
        self.update()

    def update(self):
        self.updateDynamicDrawables()

        self.setWindowTitle("OverallF: " + str(round(self.brain.overallFitness, 5)) + " LastF: " + str(round(self.brain.fitness, 5)) + " Cycle:" + str(self.brain.learnCycle))

        self.canvas.reset()
        self.canvas.addRectanges(self.rectangles)
        self.canvas.addLines(self.getLines())
        self.canvas.addStrings(self.getStrings())
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
        self.createStrings()
        self.updateLines()

    def createStaticDrawables(self):
        self.createRectangles()
        self.createLines()

    def createStrings(self):
        self.functionNames = list()

        for (layerNr, layer) in enumerate(self.brain.layers):

            if (layerNr >= len(self.neuronValueStrings)):
                self.neuronValueStrings.insert(layerNr, list())

            for (neuronNr, neuron) in enumerate(layer.neurons):
                centerPoint = self.points[layerNr][neuronNr] - Point.Point(20, 12)

                # String objects are not removed. Only updated if available
                # TODO: If this is faster then removing / creating then rewrite for Rect/Lines
                # TODO: Implement metrics to prove performance improvements
                if (neuronNr >= len(self.neuronValueStrings[layerNr])):
                    # self.strings[layerNr].insert(neuronNr, Label.Label(centerPoint, str(neuron.absoluteValue)))
                    self.neuronValueStrings[layerNr].insert(neuronNr, Label.Label(centerPoint, str(neuron.value)))
                else:
                    # self.strings[layerNr][neuronNr] = Label.Label(centerPoint, str(neuron.absoluteValue))
                    self.neuronValueStrings[layerNr][neuronNr] = Label.Label(centerPoint, str(neuron.value))

                functionNamePoint = centerPoint + Point.Point(0, 30)

                # Inputlayers do not use the activation function. Therefore hide the label
                if layerNr != 0:
                    self.functionNames.append(Label.Label(functionNamePoint, str(neuron.activeActivationName)))



    def createRectangles(self):
        # Editable vars
        layerXOffset = 10
        layerMargin = 60
        layerWidth = 60

        neuronMargin = 5

        # Do not edit below this point
        layerHeightSteps = layerWidth - neuronMargin
        neuronXOffset = 5 + layerXOffset

        neuronWidth = layerWidth - (2 * neuronMargin)
        neuronHeight = neuronWidth

        # Hidden layers are the biggest layers. Use these to calculate a offset for the input en output layer. So that it will align nicely
        maxNeuronsInLayer = self.brain.hiddenSize

        self.drawingMaxWidth = 0
        self.drawingMaxHeight = 0

        for (layerNr, layer) in enumerate(self.brain.layers):

            deltaNeuronsInLayer = maxNeuronsInLayer - len(layer.neurons)
            yOffset = (layerHeightSteps * deltaNeuronsInLayer) / 2

            layerPosition = layerNr

            xR = layerXOffset + (layerPosition * (layerWidth + layerMargin))
            yR = 10 + yOffset
            layerHeight = (len(layer.neurons) * layerHeightSteps) + neuronMargin

            rect = Rectangle.Rectangle(
                xR,
                yR,
                layerWidth,
                layerHeight
            )

            if (self.drawingMaxWidth < (xR + layerWidth)):
                self.drawingMaxWidth = (xR + layerWidth)

            if (self.drawingMaxHeight < (yR + layerHeight)):
                self.drawingMaxHeight = (yR + layerHeight)

            if (layerNr >= len(self.points)):
                self.points.insert(layerNr, list())

            self.rectangles.append(rect)

            for (neuronNr, neuron) in enumerate(layer.neurons):
                xN = (layerPosition * (layerWidth + layerMargin)) + neuronXOffset
                yN = 15 + (neuronNr * layerHeightSteps) + yOffset

                centerPoint = Point.Point(xN + (neuronWidth / 2), yN + (neuronHeight / 2))
                self.points[layerNr].insert(neuronNr, centerPoint)

                rect = Rectangle.Rectangle(
                    xN,
                    yN,
                    neuronWidth,
                    neuronHeight
                )

                self.rectangles.append(rect)

    def createLines(self):
        for (layerNr, layer) in enumerate(self.brain.layers):

            if (layerNr >= len(self.lines)):
                self.lines.insert(layerNr, list())

            for (neuronNr, neuron) in enumerate(layer.neurons):

                if (neuronNr >= len(self.lines[layerNr])):
                    self.lines[layerNr].insert(neuronNr, list())

                for (weightNr, weight) in enumerate(neuron.weights):
                    xA = layerNr - 1
                    yA = weightNr

                    xB = layerNr
                    yB = neuronNr

                    line = Line.Line(self.points[xA][yA], self.points[xB][yB])
                    line.setWeight(weight)

                    self.lines[layerNr][neuronNr].insert(weightNr, line)

    def updateLines(self):
        for (layerNr, layer) in enumerate(self.brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                for (weightNr, weight) in enumerate(neuron.weights):
                    self.lines[layerNr][neuronNr][weightNr].setWeight(weight)
