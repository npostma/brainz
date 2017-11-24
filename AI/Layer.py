class Layer:

    TYPE_INPUT = "input"
    TYPE_HIDDEN = "hidden"
    TYPE_OUTPUT = "output"

    # Collection of neurons
    neurons = list()

    # Used to identify the layers functionality
    type = None

    def __init__(self):
        self.neurons = list()
        self.type = None

    def setType(self, layerType):
        self.type = layerType

    def addNeuron(self, neuron):
        self.neurons.append(neuron)

    def size(self):
        return len(self.neurons)
