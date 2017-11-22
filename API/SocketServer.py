import socket
from PyQt4.QtCore import *

import json

HOST = '0.0.0.0'
PORT = 1337
SIZEOF_UINT32 = 4

# Socket server as a worker thread
class SocketServer(QThread):
    def __init__(self, parent=None):
        super(SocketServer, self).__init__(parent)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receiveInput(self):
        self.connection, self.address = self.socket.accept()

        recvBuffer = ""
        while 1:
            # For now accepting max message size of 2048 (Individual message!)
            dataString = self.connection.recv(2048).decode()

            if not dataString:
                break

            recvBuffer = recvBuffer + dataString
            strings = recvBuffer.split('\0')
            for message in strings[:-1]:
                try:
                    data = json.loads(message)
                    self.emit(SIGNAL(data['command']), data['input'], data['expectedOutput'])
                except ValueError as err:
                    print("Data received (" + message + ") was in incorrect format.")

            recvBuffer = strings[-1]

        self.connection.close()

    def run(self):
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        while 1:
            self.receiveInput()
