class Cell:
    # X can be seen as layerNr.
    x = 0

    # Y is the position in the layer.
    y = 0

    # Z is the weight number
    z = 0

    # Value
    weight = 0

    def __init__(self, x, y, z, weight):
        self.x = x
        self.y = y
        self.z = z
        self.weight = weight
