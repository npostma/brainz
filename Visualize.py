import sys;
import math;

class Visualize:

    brain = 0;

    def __init__(self, brain):
        self.brain = brain;

    def show(self):
        self.showValues();

    def showValues(self):
        sys.stdout.write('\n[Layer]\t\t[Type]\t[Values, .., ..]\n');

        for(layerNr, layer) in enumerate(self.brain.layers):
            if(layerNr == 0):
                sys.stdout.write('[Input]\t');
            elif(layerNr == (len(self.brain.layers) - 1)):
                sys.stdout.write('[Output]');
            else:
                sys.stdout.write('[Hidden]');

            sys.stdout.write('\tName:\t');
            for (neuronNr, neuron) in enumerate(layer.neurons):
                sys.stdout.write(neuron.name);
                self.printRestTabs(neuron.name);

            sys.stdout.write('\n')
            sys.stdout.write('\t\t\tvalue:\t');
            for(neuronNr, neuron) in enumerate(layer.neurons):
                sys.stdout.write(str(neuron.value));
                self.printRestTabs(neuron.value);

            sys.stdout.write('\n')
            sys.stdout.write('\t\t\tdelta:\t');
            for (neuronNr, neuron) in enumerate(layer.neurons):
                sys.stdout.write(str(neuron.delta));
                self.printRestTabs(neuron.delta);


            for (neuronNr, neuron) in enumerate(layer.neurons):
                if(len(neuron.weights) == 0) :
                    continue;

                sys.stdout.write('\n')
                sys.stdout.write('\t\t\tWeight:\t');
                for(weightNr, weight) in enumerate(neuron.weights):
                    for (neuronXrefNr, neuronXref) in enumerate(layer.neurons):
                       if(neuronNr == weightNr):
                            label = str(neuronXref.weights[neuronNr]);
                            sys.stdout.write(label);
                            self.printRestTabs(label);

            sys.stdout.write('\n\n')

    def printRestTabs(self, value):
        # 4 chars 6 tabs
        maxLeng = 4 * 6;
        length = len(str(value));

        numTabs = int(math.floor((maxLeng - length) / 4)) + 1;

        if ((length % 4) == 0):
            numTabs -= 1;

        for i in range(0, numTabs):
            # sys.stdout.write('[' + str(numTabs) + '-' + str(length) + ']\t');
            sys.stdout.write('\t');

    def printLayers(self):
        for (layerNr, neurons) in enumerate(self.brain.layers):
            print 'Layer ' + str(layerNr);
            for (neuronNr, neuron) in enumerate(neurons):
                print ('\r\r neuron:' + str(neuronNr));
                neuron.doPrint();

    def doPrintSettings(self):
        print('Num neurons in input layer: \t' + str(self.brain.inputSize));
        print('Num neurons in hidden layer: \t' + str(self.brain.hiddenSize));
        print('Num neurons in output layer: \t' + str(self.brain.outputSize));
        print('Num layers: \t' + str(self.brain.numLayers));
        print('\n');

