import socket
from PyQt5.QtCore import *
import json

from API import SocketClientProcessor

HOST = '0.0.0.0'
PORT = 1337
SIZEOF_UINT32 = 4


# Socket server as a worker thread
class SocketServer(QThread):
    clientProcessors = []

    learn = pyqtSignal(list, list)
    compute = pyqtSignal(list, list)

    def __init__(self, parent=None):
        super(SocketServer, self).__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        self.clientProcessors = []

    def run(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        while 1:
            self.acceptClientConnections()

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
        self.learn.emit(a, b)

    # Pass through signal from the client processor ... not sure if this is the right way
    def emitComputeSignal(self, a, b):
        self.compute.emit(a, b)
