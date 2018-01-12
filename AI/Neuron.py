import random
import math


class Neuron:
    TYPE_DEFAULT = 'default'
    TYPE_BIAS = 'bias'

    ACTIVATION_NONE = "none"
    ACTIVATION_SIGMOID = "sigmoid"
    ACTIVATION_TANH = "tanh"
    ACTIVATION_RELU = "relu"

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

    # Type
    type = ""

    # Incoming value before activation
    incomingValue = 0

    # Name to function map for fast function execution.
    activations = {}

    # Active activation function
    activeActivation = None

    # Name of the active activation function
    activeActivationName = ""

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

        self.activations = {
            self.ACTIVATION_NONE: self.__none,
            self.ACTIVATION_SIGMOID: self.__sigmoid,
            self.ACTIVATION_TANH: self.__tanh,
            self.ACTIVATION_RELU: self.__relu,
        }

        self.activeActivation = self.activations[self.ACTIVATION_SIGMOID]
        self.activeActivationName = self.ACTIVATION_SIGMOID
        self.type = self.TYPE_DEFAULT

    def doPrint(self):
        print('Neuron value: \t' + str(self.value))
        print('Weights:')
        for weight in self.weights:
            print(('\t\t\t' + str(weight)))

    def setActivationFunction(self, activationFunction):
        try:
            self.activeActivation = self.activations[activationFunction]
            self.activeActivationName = activationFunction
        except IndexError:
            return

    # Activation function outputs a value between 0 and 1
    def activate(self, incomingValue):
        self.incomingValue = incomingValue
        self.value = self.activeActivation(self.incomingValue)

    # return 1 / (1 + math.exp(-value))
    def __sigmoid(self, value):
        return 1 / (1 + math.exp((-1 * value) / 1))

    # Activation function outputs a value between -1 and 1 (Just an wrapper for math.tanh(x))
    def __tanh(self, value):
        return math.tanh(value)

    # Activation function outputs a value between 0 and inf
    def __relu(self, value):
        return max(0, value)

    # Not a activation function. Return value. Used for biased neurons and such
    def __none(self, value):
        # Dont use value. This activation function doesnt do anything.
        return self.value
