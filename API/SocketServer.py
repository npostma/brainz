import socket
from PyQt5.QtCore import *

from API import SocketClientProcessor

HOST = '0.0.0.0'
PORT = 9010


# Socket server as a worker thread
class SocketServer(QThread):
    clientProcessors = []

    learn = pyqtSignal(QThread, list, list)
    compute = pyqtSignal(QThread, list)

    def __init__(self, parent=None):
        super(SocketServer, self).__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self.clientProcessors = []

    def run(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        while 1:
            self.acceptClientConnections()

    def sendComputedResult(self, source, usedInputData, computedOutputData):
        source.sendComputedResult(usedInputData, computedOutputData)
        return

    def acceptClientConnections(self):
        print("SocketServer: Listing for a client connection.")

        connection, address = self.socket.accept()

        print("SocketServer: Client connection.")

        # Handle client connections in a new thread
        clientProcessor = SocketClientProcessor.SocketClientProcessor(connection, address)

        clientProcessor.learn.connect(self.emitLearnSignal)
        clientProcessor.compute.connect(self.emitComputeSignal)

        clientProcessor.start()
        self.clientProcessors.append(clientProcessor)

    # Pass through the signal from the client processor ... not sure if this is the right way
    def emitLearnSignal(self, a, b):
        self.learn.emit(self.sender(), a, b)

    # Pass through signal from the client processor ... not sure if this is the right way
    def emitComputeSignal(self, a):
        self.compute.emit(self.sender(), a)
