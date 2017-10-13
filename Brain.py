import math;
import Layer;
import Neuron;

class Brain:

    layers = [];

    # Number of neurons for the input layer
    inputSize = 6;
    # Number of neurons for the output layer
    outputSize = 2;
    # Number of neurons for the hidden layer
    hiddenSize = 0;
    # Number of layers
    numLayers = 0;
    # Some learningrate Todo: no clue of this is a good value for my code
    learningRate = 0.3;
    # Todo: Some value for soming. Find out what its good for
    learningMomentum = 0.9;

    def __init__(self):
        # Rule of thumb to determine wich size the neural network sould have
        if(self.inputSize > self.outputSize) :
            self.hiddenSize = self.inputSize
            self.numLayers = max(self.inputSize - self.outputSize, 3);
        else:
            self.hiddenSize = self.outputSize;
            self.numLayers = max(self.outputSize - self.inputSize, 3);

        self.createLayers();

    def createLayers(self):
        self.layers = [];
        for i in range(0, self.numLayers):
            # Every layer is a collection of neurons
            layer = Layer.Layer();

            # Is used to determine the weight of each neuron
            previousSize = self.hiddenSize;

            # Number of neurons in the current layer
            size = self.hiddenSize;

            # Input layer if i == 0
            if(i == 0):
                # First layer does not have a weight becouse there are no previous neurons
                previousSize = 0;
                size = self.inputSize;
            elif(i == 1):
                # First hidden layer. Has the weight of each input and thus it differs from the other hidden layers
                previousSize = self.inputSize;
            elif(i == (self.numLayers - 1)):
                # Output layer
                size = self.outputSize;

            for j in range(0, size):
                layer.addNeuron(Neuron.Neuron(previousSize, str(i)+'-'+str(j)));

            self.layers.append(layer);

    def compute(self, inputData):
        # Anonymous function to SUM the total value in the collection
        fsum = lambda a, b: a + b;

        if(len(inputData) != self.layers[0].size()):
            raise ValueError('Size of inputdata:' + str(len(inputData)) + ' does not match size of inputlayer:' + str(self.layers[0].size()));

        # Give input to the sensors
        for (neuronNr, inputNeuron) in enumerate(self.layers[0].neurons):
            inputNeuron.value = inputData[neuronNr];

        # Loop through the layers starting from the first hidden layer
        for i in range(1, len(self.layers)) :
            previousLayer = self.layers[i - 1];

            # Loop through the neurons in the current layer
            for (neuronNr, neuron) in enumerate(self.layers[i].neurons):

                values = [];
                for(neuronNrPrevLayer, neuronPrevLayer) in enumerate(previousLayer.neurons):
                    # The value of eachs previous neuron multiplied with the weight in the current layer
                    # This value will be stored in the current neuron. This way the value will traverse through our network
                    values.append(neuronPrevLayer.value * neuron.weights[neuronNrPrevLayer])

                value = reduce(fsum, values);
                neuron.value = self.sigmoid(value);

        # Return the output layer
        return map(lambda neuron: neuron.value, self.layers[len(self.layers) - 1].neurons);

    def learn(self, inputData, outputData):

        f = lambda a, b: a + b;

        self.compute(inputData);

        # Calculate the gradient (NL: helling) for the output layer
        for (neuronNr, neuron) in enumerate(self.layers[-1].neurons):
            neuron.delta = self.errorFunction(neuron.value, outputData[neuronNr]);

        # Bereken een gradient (helling) voor de hidden en input layers, van rechts naar links.
        # Calculate a gradient for the hidden and input layers. From right to left
        # Eg. 4 layers? Then range: 2,1,0
        layersReversed = range(len(self.layers) - 2, -1, -1);

        for (layerNr) in layersReversed:

            # NL: 1 layer naar rechts kijkend, om de delta te bereken.
            # Dus een delta tussen laatste hidden layer en output., 1e hidden layer met de 2e hidden layer, input layer met de 1e hidden layer.
            # Watch one layer to the right to calculate the delta
            # Eg. a delta between: the last layer and output, 1th hidden layer and 2th hidden layer, input layer and 1e hidden layer
            nextLayer = self.layers[layerNr + 1];

            for (neuronNr, neuron) in enumerate(self.layers[layerNr].neurons):

                deltas = [];
                for (nextNeuronNr, nextNeuron) in enumerate(nextLayer.neurons):
                    delta = nextNeuron.delta * nextNeuron.weights[neuronNr];
                    deltas.append(delta);

                error = reduce(f, deltas);

                neuron.delta = neuron.value * (1 - neuron.value) * error;

        # Herbereken het gewicht op basis van de helling
        # Recalculate the weight based on the gradient
        for(layerNr, layer) in enumerate(self.layers):
            for(neuronNr, neuron) in enumerate(layer.neurons):
                neuron.bias += self.learningRate * neuron.delta;

                if(layerNr > 0):
                    previousLayer = self.layers[layerNr-1];
                    for(weightNr, weight) in enumerate(neuron.weights):
                        previousNeuron = previousLayer.neurons[weightNr];
                        value = previousNeuron.value;
                        delta = self.learningRate * neuron.delta * value;
                        neuron.weights[weightNr] += delta + self.learningMomentum * neuron.gradient[weightNr];
                        neuron.gradient[weightNr] = delta;


    def errorFunction(self, value, expected):
        return value * (1 - value) * (expected - value);

    def sigmoid(self, value):
        return 1 / (1 + math.exp(-value));
        #return (1 / (1 + (((-1 * value) / 1) ** 2)));








