import Brain;
import copy;

class Population:

    populationSize = 12;

    brains = [];

    def __init__(self):
        self.brains = list();

        for i in range(0, self.populationSize):
            self.brains.append(Brain.Brain());

    def learn(self, inputData, outputData):
        # Let the whole population learn the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.learn(inputData, outputData);

    def compute(self, inputData):
        # Let the whole population compute the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.compute(inputData);

    def clone(self):
        return copy.deepcopy(self);