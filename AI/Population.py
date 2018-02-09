import math
import random
import time

from AI import Cell, Brain
from MRI import CLI


class Population:
    # Number of brains in this population
    populationSize = 12

    # Number of input neurons
    # This needs to be the same for all brains in this population
    inputSize = 0

    # Number of output neurons
    # This needs to be the same for all brains in this population
    outputSize = 0

    # Collection of brains
    brains = list()

    # Number of calls to the learn function
    learnIterationCounter = 0

    # Overall average of the learning function
    learnAverageTime = 0

    # Number of calls to the learn function when delay is measured
    learnIterationDelayCounter = 0

    # Overlal average of recalling the learn function when learning in batches
    learnDelayTime = 0

    # Time when the learn function is entered
    learnTimeStart = 0

    # Time when te learn function is ended.
    learnTimeEnd = 0

    def __init__(self, inputSize=6, outputSize=2, populationSize=2):
        self.brains = list()

        self.inputSize = inputSize
        self.outputSize = outputSize
        self.populationSize = populationSize

        for i in range(0, self.populationSize):
            self.brains.append(Brain.Brain(inputSize, outputSize))

    @staticmethod
    def fromBrains(brains, inputSize=6, outputSize=2):
        population = Population()
        population.brains = brains
        population.populationSize = len(brains)
        population.inputSize = inputSize
        population.outputSize = outputSize
        return population

    def learn(self, inputData, outputData):

        if len(inputData) != self.inputSize:
            raise ValueError('Size of input data:' + str(len(inputData)) + ' does not match size of input layer:' + str(
                self.layers[0].size()))

        # Let the whole population learn the same data
        start = time.time()

        self.learnTimeStart = time.time()

        if self.learnTimeStart != 0 and self.learnTimeEnd != 0:
            delayDelta = self.learnTimeStart - self.learnTimeEnd

            # Pauzes between batch learning calls do not count for 'delay'.
            # This is user interaction that takes time and need to be filtered
            if delayDelta < 3:
                self.learnIterationDelayCounter += 1;
                self.learnDelayTime = ((self.learnDelayTime * self.learnIterationDelayCounter) + delayDelta) / self.learnIterationDelayCounter

        for (brainNr, brain) in enumerate(self.brains):
            brain.learn(inputData, outputData)

        end = time.time()
        delta = end - start;

        if self.learnAverageTime == 0:
            self.learnAverageTime = delta
        else:
            self.learnAverageTime = ((self.learnAverageTime * self.learnIterationCounter) + delta)

        self.learnIterationCounter += 1

        self.learnAverageTime = (self.learnAverageTime / self.learnIterationCounter)
        self.learnTimeEnd = time.time()

        print(str(self.learnAverageTime) + '\t\t' + str(self.learnDelayTime))

    def compute(self, inputData):
        # Let the whole population compute the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.compute(inputData)

    def showOutput(self):
        for (brainNr, brain) in enumerate(self.brains):
            visual = CLI.CLI(brain)
            visual.showOutput()

    # Every couple will create 2 children with there neighbour brain on a given moment.
    def breed(self):

        # Calculate overall fitness before we start to breed.
        # Moved from learning to speed up the learning proces
        for (brainNr, brain) in enumerate(self.brains):
            brain.measureOverallFitness()

        childGenomes = list()
        childPopulation = list()

        numberOfBrains = len(self.brains)

        # Sort brain on fitness. After Breeding with neighbours this will give the best 'result'
        self.brains = sorted(self.brains, key=lambda brain: brain.overallFitness)

        for (brainNr, dadBrain) in enumerate(self.brains):
            # As long as we can find a mother brain
            # Note: For now a bit strange but for every step the mom becomes the dad :-D
            if (brainNr + 1) < numberOfBrains:
                motherBrain = self.brains[brainNr + 1]

                motherGenome = self.createGenome(motherBrain)
                dadGenome = self.createGenome(dadBrain)

                for (genomeNr, genome) in enumerate(self.crossover(motherGenome, dadGenome)):
                    childGenomes.append(genome)

        # Convert the genomes back to brains so that we can let them crunch numbers
        for (genomeNr, genome) in enumerate(childGenomes):
            childBrain = Brain.Brain.fromGenome(genome, self.inputSize, self.outputSize)
            childPopulation.append(childBrain)

        return Population.fromBrains(childPopulation, self.inputSize, self.outputSize)

    def clone(self):
        clonedPopulation = list()

        for (brainNr, brain) in enumerate(self.brains):
            genome = self.createGenome(brain)
            clonedBrain = Brain.Brain.fromGenome(genome, self.inputSize, self.outputSize)
            clonedPopulation.append(clonedBrain)

        return Population.fromBrains(clonedPopulation, self.inputSize, self.outputSize)

    def crossover(self, motherGenome, dadGenome):
        children = list()

        genomeLength = len(motherGenome)
        # A random spit. Random gives us a number between 0 and 1. So it can be used as a percentage of the length
        randomNumber = random.random()
        partOneLength = int(math.floor(genomeLength * randomNumber))
        partTwoLength = int(genomeLength - partOneLength)

        daughter = motherGenome[0:partOneLength] + dadGenome[partOneLength:genomeLength]
        son = motherGenome[0:partTwoLength] + dadGenome[partTwoLength:genomeLength]

        # Mutation part. What am I trying to do? (No clue which values, that's the fun part to analyze) so
        # - Determine how many cells are mutated this is between 0 and 5 percent
        # - Select random cells to mutate
        # - Determine how big the weights of the cells are mutated. This will be somewhere between -5 and 5%
        numberOfCellsToMutate = int(random.random() * 5)
        mutationRate = random.uniform(-0.05, 0.05)

        for (i) in range(0, numberOfCellsToMutate):
            cellNumber = int(random.uniform(0, genomeLength))
            daughter[cellNumber].weight *= mutationRate
            son[cellNumber].weight *= mutationRate

        children.append(son)
        children.append(daughter)

        return children

    # Simple function that creates a genome based on a given brain.
    # A genome consists of the weights in the network
    def createGenome(self, brain):
        genome = list()
        for (layerNr, layer) in enumerate(brain.layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                for (synapseNr, synapse) in enumerate(neuron.synapses):
                    genome.append(Cell.Cell(layerNr, neuronNr, synapseNr, synapse.weight, neuron.activeActivationName))
        return genome

    def setActivationFunction(self, layerType, activationFunction):
        for (brainNr, brain) in enumerate(self.brains):
            for (layerNr, layer) in enumerate(brain.layers):

                if(layer.type != layerType):
                    continue

                for (neuronNr, neuron) in enumerate(layer.neurons):

                    if (neuron.type != neuron.TYPE_DEFAULT):
                        # Only change the activation function for neurons that uses them
                        continue

                    neuron.setActivationFunction(activationFunction)
