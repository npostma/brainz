import random
import math

from AI import Synapse


class Neuron:
    TYPE_DEFAULT = 'default'
    TYPE_BIAS = 'bias'

    ACTIVATION_NONE = "none"
    ACTIVATION_SIGMOID = "sigmoid"
    ACTIVATION_TANH = "tanh"
    ACTIVATION_RELU = "relu"
    ACTIVATION_THRESHOLD = "threshold"

    # Name for debug identification. This will be some sort of X-Y coordinate in the network
    name = ''

    # Neuron value
    value = 0

    # Relation to list to neurons in the previous layer (Adjacency list). Also containing the weight
    synapses = list()

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

    # Reference to the layer.
    layer = None

    # Neuron number. Neurons get numbered from top to bottom.
    number = 0

    def __init__(self, layer, number: int):
        self.layer = layer
        self.number = number
        self.value = random.uniform(-1, 1)
        self.synapses = list()
        self.delta = 0
        self.bias = 0

        self.activations = {
            self.ACTIVATION_NONE: self.__none,
            self.ACTIVATION_SIGMOID: self.__sigmoid,
            self.ACTIVATION_TANH: self.__tanh,
            self.ACTIVATION_RELU: self.__relu,
            self.ACTIVATION_THRESHOLD: self.__threshold,
        }

        self.activeActivation = self.activations[self.ACTIVATION_SIGMOID]
        self.activeActivationName = self.ACTIVATION_SIGMOID
        self.type = self.TYPE_DEFAULT

    def generateSynapses(self, layer):
        for (neuronNr, neuron) in enumerate(layer.neurons):
            synapse = Synapse.Synapse(random.uniform(-1, 1), 0, neuron, self)
            self.synapses.append(synapse)

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

    # return 1 if value > 0 else 0
    def __threshold(self, value):
        return 1 if value > 0 else 0
