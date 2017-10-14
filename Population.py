import Brain
import Cell
import math
import MRI


class Population:
    # Number of brains in this population
    populationSize = 12

    brains = []

    def __init__(self, brains=None):
        self.brains = list()

        if (brains == None):
            for i in range(0, self.populationSize):
                self.brains.append(Brain.Brain())
        else:
            self.brains = brains
            self.populationSize = len(brains)

    def learn(self, inputData, outputData):
        # Let the whole population learn the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.learn(inputData, outputData)

    def compute(self, inputData, expectedOutputData):
        # Let the whole population compute the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.compute(inputData)
            brain.measureFitness(expectedOutputData)

    def showmeasureFitness(self):
        for (brainNr, brain) in enumerate(self.brains):
            print (str(brain.fitness))
        print('')

    def showOutput(self):
        for (brainNr, brain) in enumerate(self.brains):
            visual = MRI.MRI(brain)
            visual.showOutput()

    # Every couple will create 2 children with there neighbour brain on a given moment.
    def breed(self):
        childGenomes = []
        childPopulation = []

        numberOfBrains = len(self.brains)

        # Sort brain on fitness. After Breeding with neighbours this will give the best 'result'
        self.brains = sorted(self.brains, key=lambda brain: brain.fitness)

        for (brainNr, dadBrain) in enumerate(self.brains):
            # As long as we can find a mother brain
            # Note: For now a bit strange but for every step the mom becomes the dad :-D
            if ((brainNr + 1) < numberOfBrains):
                motherBrain = self.brains[brainNr + 1]

                motherGenome = self.createGenome(motherBrain)
                dadGenome = self.createGenome(dadBrain)

                for (genomeNr, genome) in enumerate(self.crossover(motherGenome, dadGenome)):
                    childGenomes.append(genome)

        # Convert the genomes back to brains so that we can let them crunch numbers
        for (genomeNr, genome) in enumerate(childGenomes):
            childBrain = Brain.Brain(genome)
            childPopulation.append(childBrain)

        return self.__class__(childPopulation)

    def crossover(self, motherGenome, dadGenome):
        children = []
        # Todo: Some kind of mutation
        genomeLength = len(motherGenome)
        partOneLength = int(math.floor(genomeLength * 0.3))
        partTwoLength = int(genomeLength - partOneLength)

        daughter = motherGenome[0:partOneLength] + dadGenome[partOneLength:genomeLength]
        son = motherGenome[0:partTwoLength] + dadGenome[partTwoLength:genomeLength]

        children.append(son)
        children.append(daughter)

        return children

    # Simple function that creates a genome based on a given brain.
    # A genome consists of the weights in the network
    def createGenome(self, brain):
        genome = list()
        for (layerNr, layer) in enumerate(brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                for (weightNr, weight) in enumerate(neuron.weights):
                    genome.append(Cell.Cell(layerNr, neuronNr, weightNr, weight))
        return genome
