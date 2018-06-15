from AI import Neuron

from . import Layer


class Brain:
    # Collection of all layers. (Input, Hidden and output)
    layers = list()

    # Number of neurons for the input layer
    inputSize = 6

    # Number of neurons for the output layer
    outputSize = 2

    # Number of neurons for the hidden layer
    hiddenSize = 0

    # Number of layers
    numLayers = 0

    # Some learning rate Todo: no clue of this is a good value for my code
    learningRate = 0.3

    # Todo: Some value for computing. Find out what its good for
    learningMomentum = 0.9

    # Keep track of the fitness score. This is the fitness of the last compute action
    fitness = 0

    # The overall fitness based on all all cases
    # Used for sorting the population
    overallFitness = 0

    # Keep track of how many times something is learned
    learnCycle = 0

    # Bias value. If None no bias is used in the brain
    biasValue = 1

    # Keep track of all the leaning data. To calculate a overall fitness we examine all the given expected outputs
    studyCases = {}

    # Number of biased neurons per layer
    biasSize = 0

    # Reversed layer sequence
    layersReversedSequence = {}

    def __init__(self, inputSize=6, outputSize=2):

        # Set default values
        self.learnCycle = 0
        self.fitness = 0
        self.overallFitness = 0
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.biasValue = 1
        self.studyCases = {}
        self.layersReversedSequence = {}

        extraNeurons = 0
        if self.biasValue:
            extraNeurons = 1

        # Rule of thumb to determine which size the neural network sould have
        # https://chatbotslife.com/machine-learning-for-dummies-part-2-270165fc1700
        # Adding one extra neuron to the layer based on the rule of thumb gives better/accurate results.
        if self.inputSize > self.outputSize:
            self.hiddenSize = self.inputSize
            self.numLayers = max((self.inputSize - self.outputSize) + extraNeurons, 3)
        else:
            self.hiddenSize = self.outputSize
            self.numLayers = max((self.outputSize - self.inputSize) + extraNeurons, 3)

        self.createLayers()

    @staticmethod
    def fromGenome(genome, inputSize=6, outputSize=2):
        brain = Brain(inputSize, outputSize)

        if genome is not None:
            for (cellNr, cell) in enumerate(genome):
                brain.layers[cell.x].neurons[cell.y].synapses[cell.z].weight = cell.weight

                # Do this only when we process the first weight. All the other names are the same/redundant
                if cell.z == 0:
                    brain.layers[cell.x].neurons[cell.y].setActivationFunction(cell.activationFunctionName)
        return brain

    def getOutput(self):
        # Return the output layer
        return [neuron.value for neuron in self.layers[len(self.layers) - 1].neurons]

    def createLayers(self):
        self.layers = list()
        for i in range(0, self.numLayers):
            # Every layer is a collection of neurons
            layer = Layer.Layer(self, i)

            # Is used to determine the weight of each neuron
            previousSize = self.hiddenSize

            # Number of neurons in the current layer
            size = self.hiddenSize

            # Input layer if i == 0
            if i == 0:
                # First layer does not have a weight becouse there are no previous neurons
                previousSize = 0
                size = self.inputSize
                layer.setType(Layer.Layer.TYPE_INPUT)
            elif i == 1:
                # First hidden layer. Has the weight of each input and thus it differs from the other hidden layers
                previousSize = self.inputSize
                layer.setType(Layer.Layer.TYPE_HIDDEN)
            elif i == (self.numLayers - 1):
                # Output layer
                size = self.outputSize
                layer.setType(Layer.Layer.TYPE_OUTPUT)
            else:
                layer.setType(Layer.Layer.TYPE_HIDDEN)

            for j in range(0, size):

                neuron = Neuron.Neuron(layer, j)

                # Create all the relations between the current neuron and all in the previous layer
                if i > 0:
                    neuron.generateSynapses(self.layers[i - 1])

                layer.addNeuron(neuron)

            if (self.biasValue is not None) and (i is not (self.numLayers - 1)):
                # All layers except output
                biasNeuron = Neuron.Neuron(layer, size)
                biasNeuron.value = self.biasValue

                layer.addBiasNeuron(biasNeuron)

            self.layers.append(layer)

        # Eg. 4 layers? Then range: 2,1,0
        self.layersReversedSequence = list(range(len(self.layers) - 2, -1, -1))

        if self.biasValue is not None:
            # If bias is used the size gets +1
            # Adding this in the end prevents adding normal neurons
            self.hiddenSize += 1
            self.inputSize += 1
            self.biasSize += 1

    def compute(self, inputData):
        # Give input to the sensors
        for (neuronNr, inputNeuron) in enumerate(self.layers[0].neurons):
            if inputNeuron.type == inputNeuron.TYPE_BIAS:
                continue

            inputNeuron.value = inputData[neuronNr]

        # Loop through the layers starting from the first hidden layer
        for i in range(1, len(self.layers)):
            previousLayer = self.layers[i - 1]

            # Loop through the neurons in the current layer
            for (neuronNr, neuron) in enumerate(self.layers[i].neurons):

                if neuron.isBias():
                    # Don't calculate the value of a bias neuron. It has no incoming synapse(s)
                    continue

                value = 0
                synapses = neuron.synapses
                for (neuronNrPrevLayer, neuronPrevLayer) in enumerate(previousLayer.neurons):
                    # The value of each previous neuron multiplied with the weight in the current layer
                    # This value will be stored in the current neuron.
                    # This way the value will traverse through our network
                    value += neuronPrevLayer.value * synapses[neuronNrPrevLayer].weight

                # SUM the total value in the collection
                neuron.activate(value)

    def learn(self, inputData, outputData):
        self.learnCycle += 1

        self.measureFitness(outputData)

        self.compute(inputData)

        self.__learn(inputData, outputData)

    def __learn(self, inputData, outputData):
        # Store all cases. This could get big. Time will tell

        # TODO: Check memory usage and performance after a lot of learning
        dataString = '-'.join(map(str, inputData))
        self.studyCases[ dataString ] = {'input': inputData, 'expectedOutput': outputData}

        layers = self.layers;

        # Calculate the gradient for the output layer
        for (neuronNr, neuron) in enumerate(layers[-1].neurons):
            neuron.delta = self.errorFunction(neuron.value, outputData[neuronNr])

        # Calculate a gradient for the hidden and input layers. From right to left
        for (layerNr) in self.layersReversedSequence:

            # Watch one layer to the right to calculate the delta
            # Eg. a delta between:
            # the last layer and output, 1th hidden layer and 2th hidden layer, input layer and 1e hidden layer
            nextLayer = layers[layerNr + 1]

            for (neuronNr, neuron) in enumerate(layers[layerNr].neurons):

                error = 0
                for (nextNeuronNr, nextNeuron) in enumerate(nextLayer.neurons):
                    if nextNeuron.type == nextNeuron.TYPE_BIAS:
                        # A bias neuron has no incoming synapse. So this can be skipped
                        continue

                    error += nextNeuron.delta * nextNeuron.synapses[neuronNr].weight

                neuron.delta = neuron.value * (1 - neuron.value) * error

        # Recalculate the weight based on the gradient
        learningRate = self.learningRate
        learningMomentum = self.learningMomentum
        for (layerNr, layer) in enumerate(layers):
            for (neuronNr, neuron) in enumerate(layer.neurons):
                neuron.bias += learningRate * neuron.delta

                if layerNr == 0:
                    continue

                previousLayer = layers[layerNr - 1]
                for (synapseNr, synapse) in enumerate(neuron.synapses):
                    previousNeuron = previousLayer.neurons[synapseNr]
                    value = previousNeuron.value
                    delta = learningRate * neuron.delta * value
                    synapse.weight += delta + learningMomentum * synapse.gradient
                    synapse.gradient = delta

    def errorFunction(self, value, expected):
        return value * (1 - value) * (expected - value)

    # Measuring fitness based on some expected data is not really testing the brain how good it is become.
    # Therefor:
    # 1 - we keep track of what its been told
    # 2 - Compute against those lines
    # 3 - Measure fitness(es)
    # 4 - calculate some super value that really tells how good this brain has become
    def measureOverallFitness(self):

        numStudyCases = len(self.studyCases.items())

        if numStudyCases == 0:
            self.overallFitness = -1
            return

        overallFitness = 0
        for (caseNr, case) in self.studyCases.items():
            self.compute(case['input'])
            print(str(case['input']) + ' --> ' + str(case['expectedOutput']))
            overallFitness += self.measureFitness(case['expectedOutput'])

        self.overallFitness = overallFitness / numStudyCases

    # Determine the fitness for now by hand. So I give it a expected output.
    # This wil NOT be used for learning but to determine how good the brain has become
    # How closer to 1 how fitter the brain is. Note!: This is for one specific task. Not the overall fitness
    def measureFitness(self, expectedOutputData):
        output = self.getOutput()

        if len(output) != len(expectedOutputData):
            raise ValueError('Size of expectedOutputData:' + str(
                len(expectedOutputData)) + ' does not match size of output:' + str(len(output)))

        error = 1
        for (i, value) in enumerate(output):
            error += abs(value - expectedOutputData[i])

        self.fitness = 1 / error

        # If local fitness is not really good, penalize
        # Todo: find out what the best values for these are
        if self.fitness < 0.9:
            self.fitness -= 0.25

        return self.fitness
