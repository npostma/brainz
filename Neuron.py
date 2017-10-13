import random;

class Neuron:

    # Name for debug indentification. This will be some sort of X-Y coordinate in the network
    name = '';

    # Neuron value
    value = 0;

    # Weight of the synapse
    weights = [];

    # Delta
    delta = 0;

    # Bias
    bias = 0;

    # Gradient (NL: Helling)
    gradient = []

    def __init__(self, numWeights, name):

        self.name = name;

        self.value = random.random();

        self.weights = [];

        for i in range(0, numWeights) :
            self.weights.append(random.random());
            self.gradient.append(0);
            
    def doPrint(self):
        print 'Neuron value: \t' + str(self.value);
        print 'Weights:';
        for weight in self.weights:
            print ('\t\t\t' + str(weight));


