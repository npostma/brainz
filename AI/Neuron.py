import random


class Neuron:
    # Name for debug indentification. This will be some sort of X-Y coordinate in the network
    name = ''

    # Neuron value
    value = 0

    # Weight of the synapse
    weights = list()

    # Gradient (NL: Helling)
    gradient = list()

    # Delta
    delta = 0

    # Bias
    bias = 0

    # Value for testing purposes
    absoluteValue = 0

    def __init__(self, numWeights, name):

        self.name = name
        self.value = random.uniform(-1, 1)
        self.weights = list()
        self.gradient = list()
        self.delta = 0
        self.bias = 0

        for i in range(0, numWeights):
            self.weights.append(random.uniform(-1, 1))
            self.gradient.append(0)

    def doPrint(self):
        print 'Neuron value: \t' + str(self.value)
        print 'Weights:'
        for weight in self.weights:
            print ('\t\t\t' + str(weight))
