class Agent:
    brain = [];

    def __init__(self):
        self.neurons = [];

    def addNeuron(self, neuron):
        self.neurons.append(neuron);

    def size(self):
        return len(self.neurons);