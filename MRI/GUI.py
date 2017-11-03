import sys
import math

from Drawable import Rectangle

# Convert brain into a set of drawable objects
class GUI:
    # Instance of the brain to scan
    brain = None

    rectangles = list()

    def __init__(self, brain):
        self.brain = brain
        self.reset();

    def reset(self):
        self.rectangles = list()

    def getRectangles(self):
        return self.rectangles

    def convertToDrawables(self):
        self.reset()

        # Editable vars
        layerXOffset = 10
        layerMargin = 60
        layerWidth = 45
        neuronMargin = 5

        # Do not edit these
        layerHeightSteps = layerWidth - neuronMargin
        neuronXOffset = 5 + layerXOffset

        neuronWidth = layerWidth - (2 * neuronMargin)
        neuronHeight = neuronWidth


        for (layerNr, layer) in enumerate(self.brain.layers):
            layerPosition = layerNr + 1;

            rect = Rectangle.Rectangle(
                layerXOffset + (layerPosition * (layerWidth + layerMargin)),
                10,
                layerWidth,
                (len(layer.neurons) * layerHeightSteps ) + neuronMargin
            );

            self.rectangles.append(rect)

            for(neuronNr, neuron) in enumerate(layer.neurons):
                rect = Rectangle.Rectangle(
                    (layerPosition * (layerWidth + layerMargin)) + neuronXOffset,
                    15 + (neuronNr * layerHeightSteps),
                    neuronWidth,
                    neuronHeight
                );

                self.rectangles.append(rect)




