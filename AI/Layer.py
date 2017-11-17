class Layer:
    # Collection of neurons
    neurons = list()

    def __init__(self):
        self.neurons = list()

    def addNeuron(self, neuron):
        self.neurons.append(neuron)

    def size(self):
        return len(self.neurons)
