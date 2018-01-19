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

    def __init__(self):
        # Editable vars
        self.layerXOffset = 10
        self.layerMargin = 60
        self.layerWidth = 60
        self.neuronMargin = 5

        # Do not edit below this point
        self.layerHeightSteps = self.layerWidth - self.neuronMargin
        self.neuronXOffset = 5 + self.layerXOffset
        self.neuronWidth = self.layerWidth - (2 * self.neuronMargin)
        self.neuronHeight = self.neuronWidth

    def getTotalWidth(self, brain):
        totalWidth = (len(brain.layers)) * (self.layerWidth + self.layerMargin)
        return totalWidth + 50

    def getTotalHeight(self, brain):
        totalHeight = 0
        for layer in brain.layers:
            height = (len(layer.neurons) + 1) * (self.neuronHeight + self.neuronMargin)
            if height > totalHeight:
                totalHeight = height
                
        return totalHeight + 50

    def getLayerHeight(self, layer):
        return (len(layer.neurons) * self.layerHeightSteps) + self.neuronMargin

    def getLayerYOffset(self, layer):
        deltaNeuronsInLayer = layer.brain.hiddenSize - len(layer.neurons)
        
        return (self.layerHeightSteps * deltaNeuronsInLayer) / 2

    def getLayerTopLeft(self, layer):
        x = self.layerXOffset + (layer.number * (self.layerWidth + self.layerMargin))
        y = 10 + self.getLayerYOffset(layer)

        return Point.Point(x, y)

    def getLayerBottomRight(self, layer):
        bottomRight = self.getLayerTopLeft(layer)
        bottomRight.setX(bottomRight.x() + self.layerWidth)
        bottomRight.setY(bottomRight.y() + self.getLayerHeight(layer))
        
        return bottomRight

    def getNeuronYOffset(self, neuron):
        return self.getLayerYOffset(neuron.layer)

    def getNeuronCenter(self, neuron):
        x = (neuron.layer.number * (self.layerWidth + self.layerMargin)) + self.neuronXOffset
        y = 15 + (neuron.number * self.layerHeightSteps) + self.getNeuronYOffset(neuron)

        return Point.Point(x + (self.neuronWidth / 2), y + (self.neuronHeight / 2))

    def getNeuronTopLeft(self, neuron):
        x = (neuron.layer.number * (self.layerWidth + self.layerMargin)) + self.neuronXOffset
        y = 15 + (neuron.number * self.layerHeightSteps) + self.getNeuronYOffset(neuron)

        return Point.Point(x, y)

    def getNeuronBotomRight(self, neuron):
        bottomRight = self.getNeuronTopLeft(neuron)
        bottomRight.setX(bottomRight.x() + self.neuronWidth)
        bottomRight.setY(bottomRight.y() + self.neuronHeight)
        
        return bottomRight

    def getNeuronLeftAnchor(self, neuron):
        leftCenterAnchor = self.getNeuronCenter(neuron)
        leftCenterAnchor.setX(leftCenterAnchor.x() - (self.layerWidth / 2))
        
        return leftCenterAnchor

    def getNeuronRightAnchor(self, neuron):
        rightCenterAnchor = self.getNeuronCenter(neuron)
        rightCenterAnchor.setX(rightCenterAnchor.x() + (self.layerWidth / 2))
        
        return rightCenterAnchor
