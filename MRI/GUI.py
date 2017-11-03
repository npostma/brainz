import sys
import math

from Drawable import Rectangle

# Convert brain into a set of drawable objects
class GUI:
    # Instance of the brain to scan
    brain = None

    def __init__(self, brain):
        self.brain = brain

    def convertToDrawables(self):
        for (i) in range(0, self.brain.numLayers):
            rect = Drawable.Rectangle();


