from Drawable import Point

# Todo: find a better name for this class ....
# Perform calculations for object positioning.


class Metrics:
    layerXOffset = 10

    layerMargin = 60

    layerWidth = 60

    neuronMargin = 5

    neuronWidth = 0

    neuronHeight = 0

    layerHeightSteps = 0

    neuronXOffset = 0

    # Flywheels preventing same calculations over and over
    totalWidth = {}
    totalHeight = {}

    layerHeight = {}
    layerYOffset = {}
    layerTopLeft = {}
    layerBottomRight = {}

    neuronCenter = {}
    neuronTopLeft = {}
    neuronBottomRight = {}
    neuronLeftAnchor = {}

    def __init__(self):
        # Editable vars
        self.layerXOffset = 10
        self.layerMargin = 60
        self.layerWidth = 60
        self.neuronMargin = 5

        self.totalWidth = {}
        self.totalHeight = {}

        self.layerHeight = {}
        self.layerYOffset = {}
        self.layerTopLeft = {}
        self.layerBottomRight = {}

        self.neuronCenter = {}
        self.neuronTopLeft = {}
        self.neuronBottomRight = {}
        self.neuronLeftAnchor = {}
        self.neuronRightAnchor = {}

        # Do not edit below this point
        self.layerHeightSteps = self.layerWidth - self.neuronMargin
        self.neuronXOffset = 5 + self.layerXOffset
        self.neuronWidth = self.layerWidth - (2 * self.neuronMargin)
        self.neuronHeight = self.neuronWidth

    def getTotalWidth(self, brain):
        if brain.__hash__() in self.totalWidth:
            return self.totalWidth[brain.__hash__()]

        totalWidth = (len(brain.layers)) * (self.layerWidth + self.layerMargin)

        self.totalWidth[brain.__hash__()] = totalWidth + 50

        return self.totalWidth[brain.__hash__()]

    def getTotalHeight(self, brain):
        if brain.__hash__() in self.totalHeight:
            return self.totalHeight[brain.__hash__()]

        totalHeight = 0
        for layer in brain.layers:
            height = (len(layer.neurons) + 1) * (self.neuronHeight + self.neuronMargin)
            if height > totalHeight:
                totalHeight = height

        self.totalHeight[brain.__hash__()] = totalHeight + 50

        return self.totalHeight[brain.__hash__()]

    def getLayerHeight(self, layer):
        if layer.number in self.layerHeight:
            return self.layerHeight[layer.number]

        self.layerHeight[layer.number] = (len(layer.neurons) * self.layerHeightSteps) + self.neuronMargin

        return self.layerHeight[layer.number]

    def getLayerYOffset(self, layer):
        if layer.number in self.layerYOffset:
            return self.layerYOffset[layer.number]

        deltaNeuronsInLayer = layer.brain.hiddenSize - len(layer.neurons)

        self.layerYOffset[layer.number] = (self.layerHeightSteps * deltaNeuronsInLayer) / 2

        return self.layerYOffset[layer.number]

    def getLayerTopLeft(self, layer):
        if layer.number in self.layerTopLeft:
            cords = self.layerTopLeft[layer.number]
            return Point.Point(cords[0], cords[1])

        x = self.layerXOffset + (layer.number * (self.layerWidth + self.layerMargin))
        y = 10 + self.getLayerYOffset(layer)

        # Storing the cords. Storing a Point object gives strange behaviour
        self.layerTopLeft[layer.number] = (x,y)

        return Point.Point(x, y);

    def getLayerBottomRight(self, layer):
        if layer.number in self.layerBottomRight:
            cords = self.layerBottomRight[layer.number]
            return Point.Point(cords[0], cords[1])

        bottomLeft = self.getLayerTopLeft(layer)

        x = bottomLeft.x() + self.layerWidth
        y = bottomLeft.y() + self.getLayerHeight(layer)

        self.layerBottomRight[layer.number] = (x, y)

        return Point.Point(x, y)

    def getNeuronYOffset(self, neuron):
        return self.getLayerYOffset(neuron.layer)

    def getNeuronCenter(self, neuron):
        if neuron.__hash__() in self.neuronCenter:
            cords = self.neuronCenter[neuron.__hash__()]
            return Point.Point(cords[0], cords[1])

        x = (neuron.layer.number * (self.layerWidth + self.layerMargin)) + self.neuronXOffset
        y = 15 + (neuron.number * self.layerHeightSteps) + self.getNeuronYOffset(neuron)

        x = x + (self.neuronWidth / 2);
        y = y + (self.neuronHeight / 2)

        self.neuronCenter[neuron.__hash__()] = (x, y)

        return Point.Point(x, y)

    def getNeuronTopLeft(self, neuron):
        if neuron.__hash__() in self.neuronTopLeft:
            cords = self.neuronTopLeft[neuron.__hash__()]
            return Point.Point(cords[0], cords[1])

        x = (neuron.layer.number * (self.layerWidth + self.layerMargin)) + self.neuronXOffset
        y = 15 + (neuron.number * self.layerHeightSteps) + self.getNeuronYOffset(neuron)

        return Point.Point(x, y);

        self.neuronTopLeft[neuron.__hash__()] = (x, y)

        return Point.Point(x, y)

    def getNeuronBottomRight(self, neuron):
        if neuron.__hash__() in self.neuronBottomRight:
            cords = self.neuronBottomRight[neuron.__hash__()]
            return Point.Point(cords[0, cords[1]])

        bottomLeft = self.getNeuronTopLeft(neuron)

        x = bottomLeft.x() + self.neuronWidth
        y = bottomLeft.y() + self.neuronHeight

        self.neuronBottomRight[neuron.__hash__()] = (x, y)

        return Point.Point(x, y)

    def getNeuronLeftAnchor(self, neuron):
        if neuron.__hash__() in self.neuronLeftAnchor:
            cords = self.neuronLeftAnchor[neuron.__hash__()]
            return Point.Point(cords[0], cords[1])

        centerPoint = self.getNeuronCenter(neuron)
        x = centerPoint.x() - (self.layerWidth / 2)
        y = centerPoint.y()

        self.neuronLeftAnchor[neuron.__hash__()] = (x, y)

        return Point.Point(x, y)

    def getNeuronRightAnchor(self, neuron):
        if neuron.__hash__() in self.neuronRightAnchor:
            cords = self.neuronRightAnchor[neuron.__hash__()]
            return Point.Point(cords[0], cords[1])

        centerPoint = self.getNeuronCenter(neuron)
        x = centerPoint.x() + (self.layerWidth / 2)
        y = centerPoint.y()

        self.neuronRightAnchor[neuron.__hash__()] = (x, y)

        return Point.Point(x, y)
