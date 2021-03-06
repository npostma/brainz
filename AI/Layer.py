class Layer:
    TYPE_INPUT = "input"
    TYPE_HIDDEN = "hidden"
    TYPE_OUTPUT = "output"

    # Collection of neurons
    neurons = list()

    # Used to identify the layers functionality
    type = None

    # bias neuron count
    biasCount = 0

    # Reference to the brain.
    layer = None

    # Layer number. Layers get numbered from left to right.
    number = 0

    def __init__(self, brain, number):
        self.brain = brain
        self.number = number
        self.neurons = list()
        self.type = None
        self.biasCount = 0

    def setType(self, layerType):
        self.type = layerType

    def addNeuron(self, neuron):
        self.neurons.append(neuron)

    def addBiasNeuron(self, neuron):
        self.neurons.append(neuron)

        # Make sure the settings are correct for a bias neuron before adding them
        neuron.type = neuron.TYPE_BIAS
        neuron.setActivationFunction(neuron.ACTIVATION_NONE)
        self.biasCount += 1

    def size(self):
        return len(self.neurons) - self.biasCount
