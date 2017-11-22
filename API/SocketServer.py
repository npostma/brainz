import socket
from PyQt4.QtCore import *
import json

HOST = '0.0.0.0'
PORT = 666
SIZEOF_UINT32 = 4


# Socket server as a worker thread
class SocketServer(QThread):
    def __init__(self, parent=None):
        super(SocketServer, self).__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receiveInput(self):
        self.connection, self.address = self.socket.accept()

        while 1:
            # For now accepting max message size of 2048 (Individual message!)
            data = self.connection.recv(2048).decode()
            if not data:
                break

            self.emit(SIGNAL("received"), data)

        self.connection.close()

    def run(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        while 1:
            self.receiveInput()
