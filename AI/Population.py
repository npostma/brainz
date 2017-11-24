import math
import random

from AI import Cell, Brain
from MRI import CLI


class Population:
    # Number of brains in this population
    populationSize = 12

    inputSize = 0

    outputSize = 0

    brains = list()

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
        # Let the whole population learn the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.learn(inputData, outputData)
            brain.measureFitness(outputData)

    def compute(self, inputData):
        # Let the whole population compute the same data
        for (brainNr, brain) in enumerate(self.brains):
            brain.compute(inputData)

    def showmeasureFitness(self):
        for (brainNr, brain) in enumerate(self.brains):
            print (str(brain.fitness))
        print('')

    def showOutput(self):
        for (brainNr, brain) in enumerate(self.brains):
            visual = CLI.CLI(brain)
            visual.showOutput()

    # Every couple will create 2 children with there neighbour brain on a given moment.
    def breed(self):
        childGenomes = list()
        childPopulation = list()

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
            cellnumber = int(random.uniform(0, genomeLength))
            daughter[cellnumber].weight *= mutationRate
            son[cellnumber].weight *= mutationRate

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
                    genome.append(Cell.Cell(layerNr, neuronNr, weightNr, weight, neuron.activeActivationName))
        return genome

    def setActivationFunction(self, layerType, activationFunction):
        for (brainNr, brain) in enumerate(self.brains):
            for (layerNr, layer) in enumerate(brain.layers):

                if(layer.type != layerType):
                    continue

                for (neuronNr, neuron) in enumerate(layer.neurons):
                    neuron.setActivationFunction(activationFunction)
