class Layer:
    # Collection of neurons
    neurons = []

    def __init__(self):
        self.neurons = []

    def addNeuron(self, neuron):
        self.neurons.append(neuron)

    def size(self):
        return len(self.neurons)
