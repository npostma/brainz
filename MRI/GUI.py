from Drawable import Rectangle, Point, Line, Label


# Convert brain into a set of drawable objects
class GUI:
    # Instance of the brain to scan
    brain = None

    # keep track of the location of a neuron (for drawing lines)
    points = list()

    rectangles = list()

    lines = list()

    strings = list()

    canvas = None

    def __init__(self, brain, canvas):

        # Static drawables
        self.rectangles = list()
        self.points = list()

        # Dynmic drawables
        self.lines = list();
        self.strings = list();

        self.brain = brain
        self.canvas = canvas
        self.reset()

        self.createStaticDrawables()

    def update(self):
        self.updateDynamicDrawables()

        self.canvas.reset()
        self.canvas.addRectanges(self.rectangles)
        self.canvas.addLines(self.lines)
        self.canvas.addStrings(self.getStrings())
        self.canvas.repaint()

    def reset(self):
        self.lines = list()


    def getRectangles(self):
        return self.rectangles

    def getLines(self):
        return self.lines

    def getStrings(self):
        strings = list()
        for (i, stringList) in enumerate(self.strings):
            for (j, string) in enumerate(stringList):
                strings.append(string)

        return strings

    def updateDynamicDrawables(self):
        self.reset()
        self.createLines()
        self.createStrings()

    def createStaticDrawables(self):
        self.createRectangles()

    def createStrings(self):
        for (layerNr, layer) in enumerate(self.brain.layers):

            if (layerNr >= len(self.strings)):
                self.strings.insert(layerNr, [])

            for (neuronNr, neuron) in enumerate(layer.neurons):
                centerPoint = self.points[layerNr][neuronNr]
                # String objects are not removed. Only updated if available
                # TODO: If this is faster then removing / creating then rewrite for Rect/Lines
                # TODO: Implement metrics to prove performance improvements
                if (neuronNr >= len(self.strings[layerNr])):
                    self.strings[layerNr].insert(neuronNr, Label.Label(centerPoint, str(neuron.value)))
                else:
                    self.strings[layerNr][neuronNr] = Label.Label(centerPoint, str(neuron.value))

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

        for (layerNr, layer) in enumerate(self.brain.layers):

            deltaNeuronsInLayer = maxNeuronsInLayer - len(layer.neurons)
            yOffset = (layerHeightSteps * deltaNeuronsInLayer) / 2

            layerPosition = layerNr + 1

            rect = Rectangle.Rectangle(
                layerXOffset + (layerPosition * (layerWidth + layerMargin)),
                10 + yOffset,
                layerWidth,
                (len(layer.neurons) * layerHeightSteps) + neuronMargin
            )

            if (layerNr >= len(self.points)):
                self.points.insert(layerNr, [])

            self.rectangles.append(rect)

            for (neuronNr, neuron) in enumerate(layer.neurons):
                x = (layerPosition * (layerWidth + layerMargin)) + neuronXOffset
                y = 15 + (neuronNr * layerHeightSteps) + yOffset

                centerPoint = Point.Point(x + (neuronWidth / 2), y + (neuronHeight / 2))
                self.points[layerNr].insert(neuronNr, centerPoint)

                rect = Rectangle.Rectangle(
                    x,
                    y,
                    neuronWidth,
                    neuronHeight
                )

                self.rectangles.append(rect)

    def createLines(self):
        for (layerNr, layer) in enumerate(self.brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                for (weightNr, weight) in enumerate(neuron.weights):
                    xA = layerNr - 1
                    yA = weightNr

                    xB = layerNr
                    yB = neuronNr

                    line = Line.Line(self.points[xA][yA], self.points[xB][yB])
                    line.setWeight(weight)

                    self.lines.append(line)