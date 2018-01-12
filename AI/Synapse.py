# Create a graph of the network so now we can use all kinds of traversing when needed "-)
class Synapse:
    # Weight of the synapse
    weight = 0

    # Gradient value
    gradient = 0

    # Left neuron (Target)
    leftNeuron = None

    # Right neuron (Parent/Source)
    rightNeuron = None

    def __init__(self, weight, gradient, leftNeuron, rightNeuron):
        self.weight = weight
        self.leftNeuron = leftNeuron
        self.rightNeuron = rightNeuron
