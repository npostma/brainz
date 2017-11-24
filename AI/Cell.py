class Cell:
    # X can be seen as layerNr.
    x = 0

    # Y is the position in the layer.
    y = 0

    # Z is the weight number
    z = 0

    # Value
    weight = 0

    # For the sake of simplicity, we store this here. Con: causes redundant data for a neuron. Not harmfull, just waste
    activatationFunctionName = ""

    def __init__(self, x, y, z, weight, activationFunctionName):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight
        self.activationFunctionName = activationFunctionName
